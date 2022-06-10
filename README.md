# Installation of requirements

python -m pip install -r requirements.txt

python manage.py makemigrations

python manage.py makemigrations api

python manage.py migrate

# for create a user

python manage.py createsuperuser

# Run server

- Don't forgot to run your python environnement
- Don't forgot to launch mysql server

python manage.py runserver

# api documentation

http://your_address/docs/ for the built-in api documentation
http://your_address/swagger-docs/ for the swagger api documentation

# User creation

## Sign up
    ```
    auth = {
        username: '',
        first_name: '',
        last_name: '',
        password: '',
        email: '',
        groups: ''
    }

    signUp(auth: any): Observable<any> {
        return this.http.post<any>(`your_address/users/?format=json`, auth);
    }```

## Sign in
```
auth = {
  username: '',
  password: ''
}

signIn(auth: any): Observable<any> {
  return this.http.post<any>(`your_address/api-token-auth/`, auth);
}```

You need to add authentification token to all secure route header like this
  
('Authorization', "token "+ your_token)


# Sondage

## create sondage

url : http://your_address/sondage/setSondage/

### sample of json to send
```
{
    "user": 1,
    "description": "Dans ce sondage nous essayons de comprendre l'utilisation ainsi que les consequence de réseaux sociaux sur notre societé",
    "title": "Sondage sur l'utilisation des réseaux sociaux au Mali",
    "questions": [
        {
            "type": 0,
            "description": "",
            "question": "Avez vous déja utilisé un reseau social ?",
            "answers": [
                {
                    "label": "Oui"
                },
                {
                    "label": "Non"
                }
            ]
        },
        {
            "type": 1,
            "description": "",
            "question": "Si vous avez déja utilisé lesquels ?",
            "answers": [
                {
                    "label": "TikTok"
                },
                {
                    "label": "Facebook"
                },
                {
                    "label": "Twitter"
                },
                {
                    "label": "whatsapp"
                }
            ]
        }
    ]
}```

## get sondage

url : http://your_address/sondage/1/getSondage/

### Exemple of sondage
```
{
    "id": 1,
    "user": 1,
    "description": "Dans ce sondage nous voudrions connaitre les language de programmation les plus
utilises au Mali", "title": "Language de programmation au Mali", "questions": [{"id": 1, "type": 1, "question":
"Quelle language avez vous déja utilisee ?",
    "reponses": [
        {
            "id": 1,
            "label": "C++"
        },
        {
            "id": 2,
            "label": "Java"
        },
        {
            "id": 3,
            "label": "Python"
        },
        {
            "id": 4,
            "label": "C#"
        },
        {
            "id": 5,
            "label": "JS"
        },
        {
            "id": 6,
            "label": "TypeScript"
        }
    ]
}
,
{
    "id": 2,
    "type": 2,
    "question": "Quelle language vous prevoyer d'apprendre ?",
    "reponses": [
        {
            "id": 7,
            "label": "C++"
        },
        {
            "id": 8,
            "label": "R"
        },
        {
            "id": 9,
            "label": "SQL"
        },
        {
            "id": 10,
            "label": "SCALA"
        }
    ]
}
]
}```

## set answer

url : http://your_address/sondage/setAnswer/

### sample data
```
{
    "email": "test123@gmail.com",
    "sondage": 7,
    "answers": [
        {
            "id_question": 5,
            "question_label": 17,
            "response": ""
        },
        {
            "id_question": 6,
            "question_label": 20,
            "response": "",
            //You add responses if the question is a multiple choice with array of checked values id
            "responses":[4,2,8]
        }
    ]
}```
