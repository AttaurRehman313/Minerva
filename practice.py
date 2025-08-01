from key import mistral_key
from langchain_mistralai.chat_models import ChatMistralAI 
import json
from flask import Flask, request, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint
import pickle
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learning.db'  # Use your database URL
db = SQLAlchemy(app)

llm=ChatMistralAI(mistral_api_key=mistral_key)

### user table
class User(db.Model):
    user_id = db.Column(db.String(36), primary_key=True)

#### conversation table
class Conversation(db.Model):
    conversation_id = db.Column(db.String(16), primary_key=True)
    user_id = db.Column(db.String(16), db.ForeignKey('user.user_id'),primary_key=True)
    conversation_memory = db.Column(db.LargeBinary)
    ### it is used for composit key 
    __table_args__ = (
        PrimaryKeyConstraint( 'conversation_id','user_id'), {}
    )

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/abcd1', methods=['POST'])
def chat():
    if request.method=='POST':

        user_id=request.json['user_id']
        conv_id=request.json['conv_id']
        prompt=request.json['prompt']
        #### if user enter null value give for any input tabe
        if user_id==None or conv_id==None or prompt==None or user_id=='' or conv_id=='' or prompt=='':
            return "enter value for empty input tab"
        

        guide_promt='''\nGenerate a valid HTML response without any descriptive text\n
        or unnecessary characters. The output must be clean and in HTML format,\n
        intended for direct use on a webpage. Avoid including any extra\n
        descriptive text or line breaks (\n) that could cause issues\n
        when integrated into a webpage. Your response must be enclosed in HTML tags.\n
        Use your knowledge and integrate all the tags necessary for understanding \n
        such as heading and other ones. Avoid pre and after extra text generated \n
        by your model.
        '''

        res_prompt=prompt+guide_promt

        user=User.query.filter_by(user_id=user_id).first()
        if user:
            conver= Conversation.query.filter_by(user_id=user_id,conversation_id=conv_id).first()
            if conver:
                memory=pickle.loads(conver.conversation_memory)
                conversation=ConversationChain(llm=llm,memory=memory) 
                try:     
                    response=conversation.predict(input=res_prompt)
                except Exception as m:
                    response=f"it is a mistral llm problem check Api key or iternet issue {m}"
                
                user.memory=pickle.dumps(conversation.memory)
                db.session.commit()
                return response

            else:
                memory=ConversationBufferMemory()
                conversation=ConversationChain(llm=llm,memory=memory)
                try:
                    response=conversation.predict(input=res_prompt)
                except Exception as m:
                    response=f"it is a mistral llm problem check Api key or iternet issue {m}"
                
                new_conv=Conversation(user_id=user_id,conversation_id=conv_id,conversation_memory=pickle.dumps(conversation.memory))
                db.session.add(new_conv)
                
                db.session.commit()
                return response
            
        else:
            memory=ConversationBufferMemory()
            conversation=ConversationChain(llm=llm,memory=memory)
            try:
                response=conversation.predict(input=res_prompt)
            except Exception as m:
                response=f"it is a mistral llm problem check Api key or iternet issue {m}"
            ## add data in user table
            new_data=User(user_id=user_id)
            db.session.add(new_data)
            ### add data in coversation table
            new_conv=Conversation(user_id=user_id,conversation_id=conv_id,conversation_memory=pickle.dumps(conversation.memory))
            db.session.add(new_conv)
            db.session.commit()
            return response
    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)