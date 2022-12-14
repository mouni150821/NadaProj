
from flask import *
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient,_container_client
from flask_sqlalchemy import SQLAlchemy

import os

#from sqlalchemy import create_engine
import psycopg2
import pandas as pd




storage_account_key = "x3uGxcHOPRBGr6ubganIRxZwH/OtDyVFE6SoekthOBRd4yq57I+o07lWMrSkXxbck6rM+5vIXB+++AStjwIrAQ=="
storage_account_name = "tutoriel"
connection_string = "DefaultEndpointsProtocol=https;AccountName=tutoriel;AccountKey=x3uGxcHOPRBGr6ubganIRxZwH/OtDyVFE6SoekthOBRd4yq57I+o07lWMrSkXxbck6rM+5vIXB+++AStjwIrAQ==;EndpointSuffix=core.windows.net"
container_name = "photos"
def uploadToBlobStorage(file,filename):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    blob_client.upload_blob(file)
    print(f"Uploaded {filename}.")
# calling a function to perform upload
#uploadToBlobStorage(r"C:\Users\LOMRI Yassine\Documents\GitHub\NadaProj\img\uploads\Logo nada.png",'Logo.png')

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///worddb.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://oepenkfltvvqdc:ece8e7635ef8e5b63b66fc9ccf0855aee94de4e2c5f38309706092626c57136a@ec2-63-32-248-14.eu-west-1.compute.amazonaws.com:5432/deq4mlq9voec8h'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///https://drive.google.com/file/d/1zFFz1-eX9Jk_JHrsjM5tYyx5huM8npGx/view?usp=share_link'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Word(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    string = db.Column(db.String(50))
    context = db.Column(db.String(50), default=None)
    num_add = db.Column(db.Integer, default= 0)

    def __repr__(self):
        return f"Word(string = {self.string}, added = {self.added})"

class Contributions(db.Model):
    string = db.Column(db.String(50), primary_key=True)
    nombre = db.Column(db.Integer)

    def __repr__(self):
        return f"Contribution(string = {self.string}, added = {self.added})"

'''
with app.app_context() :
    
    #result2 = Contributions.query.filter_by(string="compteur").first()
    df = pd.read_excel("DicLsf.xlsx")
    column1 = df.columns[0]
    column2 = df.columns[1]
    column3 = df.columns[2]
    print(column2)
    #print("-" * len(column1))
    for index, row in df.iterrows():
        db.session.add(Word(id=row[column1],string=str(row[column2]), context=str(row[column3])))
    db.session.commit()
        #print(row[column1])
    
    engine = create_engine('postgresql+psycopg2://ecmnjnejxzpejf:ef65539509a755bdef8f127e2c9001ae6fd0b68d365e15be647469c89a2803dd@ec2-63-32-248-14.eu-west-1.compute.amazonaws.com:5432/d7tffuois6u87f')
    with pd.ExcelFile('DicLsf.xlsx') as xls :
        df= pd.read_excel(xls)
        df.to_sql(name='Word',con= engine,if_exists='append',index=False)
    #db.session.commit()
#print(result2.nombre)
'''
'''
with app.app_context() :
    db.create_all()
    db.session.add(Contributions(string="compteur", nombre=0))
    db.session.commit()
'''
'''
connect_str = "DefaultEndpointsProtocol=https;AccountName=tutoriel;AccountKey=x3uGxcHOPRBGr6ubganIRxZwH/OtDyVFE6SoekthOBRd4yq57I+o07lWMrSkXxbck6rM+5vIXB+++AStjwIrAQ==;EndpointSuffix=core.windows.net"
#os.getenv('AZURE_STORAGE_CONNECTION_STRING') # retrieve the connection string from the environment variable
container_name = "photos" # container name in which images will be store in the storage account

blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # create a blob service client to interact with the storage account
try:
    container_client = blob_service_client.get_container_client(container=container_name) # get container client to interact with the container in which images will be stored
    container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
except Exception as e:
    print(e)
    print("Creating container...")
    container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist
'''




@app.route("/")
def home():
    result = Contributions.query.filter_by(string="compteur").first()
    compteur=result.nombre
    return render_template('home.html', compteur=compteur)


@app.route("/mentions-legales")
def ml():
    return render_template('ml.html')


app.config["ALLOWED_IMAGE_EXTENSONS"] = ["M4V","MP4","MOV"]

def allowed_video(filename) :
    if not "." in filename :
        return False
    ext= filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSONS"] :
        return True
    else :
        return False

@app.route("/upload-image", methods= ["GET","POST"])
def upload_image():

    if request.method=="POST" :

        if request.files:

           image = request.files["image"]

           if image.filename== "" :
               print("Image must have a filename")
               return redirect(request.url, text = "Votre vid??o doit comporter un nom.")

           if not allowed_video(image.filename) :
               print("That image ext is not allowed")
               redirect(request.url, text ="Ce type de fichier n'est pas accept??.")

           else :
                filename= secure_filename(image.filename)
                #image.save(os.path.join(app.config["IMAGE_UPLOAD"], filename))
                try:
                    uploadToBlobStorage(image,filename)
                    print("Image Saved")
                except Exception as e:
                    print(e)
                    print("Ignoring duplicate filenames")  # ignore duplicate filename





           #image.save(os.path.join(app.config["IMAGE_UPLOAD" ], image.filename) )

           return redirect(request.url, texte = "Votre vid??o a bien ??t?? enregistr??e, merci pour votre contribution !")


    return render_template('upload-image.html')



@app.route("/contribuer", methods= ["GET","POST"])
def contribuer():
    with app.app_context():
        if request.method=="POST" :

            if request.files:

               video = request.files["video"]
               print(request.form["videoword"])
               if video.filename== "" :
                   print("Video must have a filename")
                   return render_template('contribute.html', text = "Votre vid??o doit comporter un nom.")

               if request.form["videoword"] == "":
                   print("Video must have a filename")
                   return render_template('contribute.html', text="Veuillez entrer le mot ou l'expression correspondant ?? la vid??o.")

               if not allowed_video(video.filename) :
                   print("That video ext is not allowed")
                   return render_template('contribute.html', text ="Ce type de fichier n'est pas accept??.")

               else :
                    success= False
                    count=0
                    blob_service_client=BlobServiceClient.from_connection_string(connection_string)
                    container_client = blob_service_client.get_container_client(container=container_name)
                    blob_items = container_client.list_blob_names()  # list all the blobs in the container
                    filename = request.form["videoword"].lower() + "_" + str(count) + "." + video.filename.rsplit(".", 1)[1]
                    while success ==False :
                        if filename not in blob_items :
                            success= True
                        else :
                            count+=1
                            filename = request.form["videoword"].lower() + "_" + str(count) + "." + video.filename.rsplit(".", 1)[1]

                    try:
                        print("essai pour count: "+str(count))
                        uploadToBlobStorage(video,filename)
                        print("Valeur passe ?? true")
                        success=True
                        print("Video Saved")
                        result=Word.query.filter(Word.string.ilike(str(request.form["videoword"]))).first()
                        result2 = Contributions.query.filter_by(string="compteur").first()
                        result2.nombre += 1
                        db.session.commit()
                        if not result :
                            print("No such word")
                        else :
                            print("Word found" +str(request.form["videoword"]+"--the other is "+ result.string))
                            result.num_add+=1
                            #check = Contributions.query.filter_by(string="compteur").first()
                            #print("Nouvelle valeur :"+str(check.nombre))
                            db.session.commit()
                            #check = Contributions.query.filter_by(string="compteur").first()
                            #print("Nouvelle valeur 2 :" + str(check.nombre))
                        return render_template('contribute.html',
                                               text="Votre vid??o a bien ??t?? enregistr??e, merci pour votre contribution !")
                    except Exception as e:
                        print(e)
                        print("Ignoring duplicate filenames")  # ignore duplicate filename

        return render_template('contribute.html',mot=request.args.get("text"))



@app.route('/mots-manquants')
def mots_manquants():
    result = Word.query.order_by(Word.id).filter(Word.num_add <3 )
    #result = Word.query.order_by(Word.id).all()
    words = result
    for word in words:
        print(word.string)
    #print(words[0].string+ str(words[0].num_add))
    #print(words.string + str(words.num_add))
    return render_template('mots_manquants.html', words=words)


if __name__ == '__main__':
    app.run(debug=True)
