<template>
  <v-app>
    <v-container>
      <v-row justify="center">
        <v-col
          cols="12"
          md="5"
        >
          <base-material-card>
            <template v-slot:heading>
              <div class="display-2 font-weight-light">
                Добро пожаловать
              </div>
            </template>

            <v-form
              class="login"
              @submit.prevent="login"
            >
              <v-container class="py-0">
                <v-row>
                  <v-col
                    cols="12"
                    md="5"
                  >
                    <v-text-field
                      v-model="name"
                      label="Логин"
                      class="purple-input"
                    />
                  </v-col>
                  <div class="mx-3" />
                  <v-col
                    cols="12"
                    md="5"
                  >
                    <v-text-field
                      v-model="password"
                      :type="show1 ? 'text' : 'password'"
                      label="Пароль"
                      class="purple-input"
                    />
                  </v-col>
                  <v-col
                    cols="12"
                    class="text-center"
                  >
                    <v-btn
                      color="success"
                      class="mr-0"
                      type="submit"
                    >
                      Войти
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
          </base-material-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
  export default {
    data () {
      return {
        name: '',
        password: '',
      }
    },
    methods: {
      login: function () {
        const login = this.name
        const password = this.password
        console.log(name, password)
        this.$store.dispatch('login', { login, password })
          .then(() => this.$router.push('/'))
          .catch(err => console.log(err))
      },
    },
  }
</script>
