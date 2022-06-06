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

# User creation

## Sign up

    auth = {
        username: '',
        first_name: '',
        last_name: '',
        password: '',
        email: '',
        groups: ''
    }
    signUp(auth: any): Observable<any> {
        return this.http.post<any>(`${environment.api}users/?format=json`, customer);
    }

## Sign in

- auth = {
  username: '',
  password: ''
  }
  signIn(auth: any): Observable<any> {
  return this.http.post<any>(`${environment.api}api-token-auth/`, auth);
  }
- You need to add authentification token to all secure route
  this.xhr = req.clone({
  headers: req.headers.set('Authorization', "token "+ this.token)
  });

## User other route

- getUser(id): Observable<any> {
  return this.http.get<any>(`${environment.api}users/free`);
  }
  deleteUsers(id): Observable<any> {
  return this.http.delete<any>(`${environment.api}users/${id}/?format=json`);
  }

  createGroup(group: any): Observable<any> {
  return this.http.post<any>(`${environment.api}group/?format=json`, group);
  }
  getGroups(): Observable<any> {
  return this.http.get<any>(`${environment.api}group/?format=json`);
  }

  deleteUser(id): Observable<any> {
  return this.http.delete<any>(`${environment.api}users/${id}/`);
  }

# Sondage

## create sondage

- url : http://127.0.0.1:8000/sondage/setSondage/

### sample of json to send

- { "user": 1, "description": "Dans ce sondage nous voudrions vos idée de business",
  "title": "Quelle business en 2022 au Mali", "questions": [
  { "type": 1, "description":"","question": "Avez vous deja lancé un business ?",
  "answers": [{ "label": "Oui"}, { "label": "Non"}]},
  {"type": 2,"description":"", "question": "Si vous devez en lancé lequel choisiriez vous ?",
  "answers": [{"label": "Agriculture"}, {"label": "pisciculture"}, {"label": "Elevage"},
  {"label": "Petit commerce"}]}
  ]
  }

## get sondage

- url : http://127.0.0.1:8000/sondage/1/getSondage/

### Exemple of response

- {"id": 1, "user": 1, "description": "Dans ce sondage nous voudrions connaitre les language de programmation les plus
  utilises au Mali", "title": "Language de programmation au Mali", "questions": [{"id": 1, "type": 1, "question":
  "Quelle language avez vous deja utilise ?", "reponses": [{"id": 1, "label": "C++"}, {"id": 2, "label":
  "Java"}, {"id": 3, "label": "Python"}, {"id": 4, "label": "C#"}, {"id": 5, "label": "JS"}, {"id": 6, "label":
  "TypeScript"}]}, {"id": 2, "type": 2, "question": "Quelle language vous prevoyer d'apprendre ?", "reponses": [{"id": 7,
  "label": "C++"}, {"id": 8, "label": "R"}, {"id": 9, "label": "SQL"}, {"id": 10, "label": "SCALA"}]}]}

## set answer

- url : http://127.0.0.1:8000/sondage/setAnswer/

### sample data

- { "email": "test123@gmail.com", "sondage": 1, "answers": [
  { "id_question": 1, "question_label":12, "label":"if other or string"},
  { "id_question": 7, "question_label":10, "label":"if other or string"},
  { "id_question": 6, "question_label":11, "label":"if other or string"}
  ]
  }
