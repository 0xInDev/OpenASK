<script>
  import axios from 'axios';

  export default {
    data () {
      return {
        Sondage: [],
        Sondage_result: [],
        person_sondage_data: {
        },
        drawer: false,
        dialog: false,
        dialog2: false,
        username: '',
        password: '',
        errorMesaage: '',
        loggedIn: false,
        loading: false,
        apiUrl: this.$config.public.API_URL ?? 'http://127.0.0.1:8000'
      }
    },
    mounted () {
      console.log(this.$config.public.API_URL)
      if (localStorage.getItem('token') !== null && localStorage.getItem('token') !== 'undefined') {
        this.dialog = false
        this.loggedIn = true
        this.getSondage()
      } else {
        this.dialog = true
      }
    },
    methods: {
      login () {
        this.errorMesaage = ''
        axios.post(this.apiUrl + '/api-token-auth/', {
          username: this.username,
          password: this.password
        }).then(response => {
          localStorage.setItem('token', response.data.token)
          this.loggedIn = true
          this.dialog = false
          this.getSondage()
        }).catch(error => {
          this.errorMesaage = error.response.data.non_field_errors[0]
          console.log(error)
        })
      },
      getSondage () {
        let config = {
          headers: {
            'Authorization': 'Token ' + localStorage.getItem('token')
          }
        }
        this.loading = true
        axios.get(this.apiUrl + '/sondage/', config)
          .then(response => {
            this.loading = false
            this.Sondage = response.data
          })
          .catch(error => {
            console.log(error)
            this.loading = false
          })
      },
      getSondageResult (sondage) {
        let config = {
          headers: {
            'Authorization': 'Token ' + localStorage.getItem('token')
          }
        }
        this.loading = true
        axios.get(this.apiUrl + '/sondage/' + sondage + '/result/', config)
          .then(response => {
            this.loading = false
            this.Sondage_result = response.data.sondage.responses
          })
          .catch(error => {
            this.loading = false
            console.log(error)
          })
      },
      showPerson(data) {
        this.person_sondage_data = data
        this.dialog2 = true
      },
      logout () {
        this.person_sondage_data = {}
        this.Sondage_result = []
        this.Sobdage = []
        localStorage.removeItem('token')
        this.dialog = true
        this.loggedIn = false
      }
    },
  }
</script>

<template>
  <div>
    <v-app 
      theme="dark"
      color="primary"
      >
      <v-app-bar :elevation="2"
        width="100%"
        v-if="loggedIn"
      >
        <v-toolbar-title class="ml-5 text-h6">OpenASK - Tableau de board</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon
          @click="logout"
        >
          <v-icon>mdi-logout</v-icon>
        </v-btn>
      </v-app-bar>
      
      <v-row v-if="loggedIn">
        <v-col cols="12" v-if="Sondage.length > 0">
          <v-container 
            fluid
            class="ma-0 d-flex pt-4 mt-16"
          >
            <v-row>
              <v-col cols="12">
                <v-card
                  class="mx-auto"
                >
                  <v-card-title>
                    <span class="headline">Sondage</span>
                  </v-card-title>
                  <v-card-text>
                    <v-select
                      model-value="Sondage"
                      :items="Sondage"
                      item-title="libelle"
                      item-value="id"
                      label="Sondage"
                      @update:model-value="getSondageResult"
                    ></v-select>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-col>
        <v-col cols="12" class="d-flex justify-center" v-if="loading">
          <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
        </v-col>
        <v-col cols="12" v-if='Sondage_result.length > 0'>
          <v-container 
          fluid
          class="ma-0 pa-20 pt-0 mt-0"
          >
          <v-table>
            <thead>
              <tr>
                <th class="text-left">
                  Author
                </th>
                <th class="text-left">
                  Email
                </th>
                <th class="text-left">
                  Phone
                </th>
                <th class="text-left">
                  Date
                </th>
                <th class="text-center"
                  width="120">
                  Action
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in Sondage_result"
                :key="item.name"
              >
                <td>Person {{ item.author.id }}</td>
                <td>{{ item.author.email }}</td>
                <td>{{ item.author.phone_number }}</td>
                <td>{{ new Date(item.created_at).toLocaleString() }}</td>
                <td>
                  <v-btn
                    color="secondary"
                    class="mr-2"
                    @click="showPerson(item)"
                    >
                    <v-icon>mdi-eye</v-icon>
                    Voir
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-container>
        </v-col>
      </v-row>
      <!-- Create authentication dialog no auto close -->
      <v-dialog v-model="dialog" max-width="420px" persistent>
        <v-card class="pa-4 rounded-xl">
          <v-card-title class="headline text-center text-h6">Tableau de board</v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12" class="pa-0">
                  <v-text-field
                    v-model="username"
                    label="Utilisateur"
                    name="username"
                    type="text"
                    variant="outlined"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" class="pa-0">
                  <v-text-field
                    v-model="password"
                    label="Mot de passe"
                    name="password"
                    type="password"
                    variant="outlined"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" class="pa-0">
                  <v-alert
                    v-if="errorMesaage"
                    type="error"
                  >
                    {{ errorMesaage }}
                  </v-alert>
                </v-col>
                <v-col cols="12" class="pa-4 justify-center d-flex">
                  <v-btn
                    color="primary"
                    size="large"
                    variant="outlined"
                    @click="login"
                    >
                    Connecter
                  </v-btn>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-card>
      </v-dialog>
      <!-- Create new dialog for person sondage result -->
      <v-dialog v-model="dialog2" max-width="700px">
        <v-card>
          <v-card-title class="headline">Person {{ person_sondage_data.email }}</v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <p>
                  Responses: 
                  <div v-for="response in person_sondage_data.author_response">
                    <label>
                      <strong>{{ response.question_libelle }}</strong> <br/>
                    </label>
                    <label>
                      <span class="bg-info" v-if="response.response_value.question?.type_response === 2 || response.response_value.question?.type_response === 3">
                        {{ response?.response_value?.libelle }}
                      </span>
                      <span class="bg-secondary" v-else-if="response.response_value.question?.type_response === 0">
                        {{ response.response_value.libelle }}
                      </span>
                      <span class="bg-primary" v-else-if="response.response_value.question?.type_response === 1">
                        <span v-for="item in response?.response_value">
                          {{ item.libelle }} <br/>
                        </span>
                      </span>
                      <span class="bg-info" v-else>
                        {{ response.response_value }}
                      </span>

                    </label>
                  </div>
                </p>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="dialog2 = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-app>
  </div>
</template>