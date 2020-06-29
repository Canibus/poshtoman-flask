<template>
  <v-container
    id="dashboard"
    fluid
    tag="section"
  >
    <v-row>
      <v-col
        cols="12"
        md="12"
      >
        <base-material-card class="px-5 py-3">
          <template v-slot:heading>
            <v-tabs
              v-model="tabs"
              background-color="transparent"
              slider-color="white"
            >
              <span
                class="subheading font-weight-light mx-3"
                style="align-self: center"
              >Разработка:</span>
              <v-tab class="mr-3">
                <v-icon class="mr-2">
                  mdi-bug
                </v-icon>
                Баги
              </v-tab>
              <v-tab class="mr-3">
                <v-icon class="mr-2">
                  mdi-code-tags
                </v-icon>
                Логи
              </v-tab>
              <v-tab>
                <v-icon class="mr-2">
                  mdi-phone
                </v-icon>
                Рассылка
              </v-tab>
            </v-tabs>
          </template>

          <v-tabs-items
            v-model="tabs"
            class="transparent"
          >
            <v-tab-item
              v-for="n in 3"
              :key="n"
            >
              <v-card-text>
                <v-row>
                  <v-col
                    cols="2"
                    class="text-right"
                  />
                </v-row>
                <template v-for="(task, i) in tasks[tabs]">
                  <v-row
                    :key="i"
                    align="center"
                  >
                    <v-col cols="1">
                      <v-list-item-action>
                        <v-checkbox
                          v-model="task.value"
                          color="secondary"
                        />
                      </v-list-item-action>
                    </v-col>

                    <v-col cols="9">
                      <div
                        class="font-weight-light"
                        v-text="task.text"
                      />
                    </v-col>

                    <v-col
                      cols="2"
                      class="text-right"
                    >
                      <v-icon class="mx-1">
                        mdi-pencil
                      </v-icon>
                      <v-icon
                        color="error"
                        class="mx-1"
                      >
                        mdi-close
                      </v-icon>
                    </v-col>
                  </v-row>
                </template>
              </v-card-text>
            </v-tab-item>
          </v-tabs-items>
        </base-material-card>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-dialog
        v-model="dialog"
        persistent
        max-width="600px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            color="blue"
            dark
            v-bind="attrs"
            v-on="on"
          >
            Добавить баг
          </v-btn>
        </template>
        <v-card>
          <v-card-title>
            <span class="headline">Добавить баг</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    label="Email для связи"
                    required
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <v-textarea
                    label="Описание"
                    required
                  />
                </v-col>
              </v-row>
            </v-container>
            <small>*поля обязательные к заполнению</small>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn
              color="blue darken-1"
              text
              @click="dialog = false"
            >
              Закрыть
            </v-btn>
            <v-btn
              color="blue darken-1"
              text
              @click="dialog = false"
            >
              Сохранить
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'DashboardDashboard',

    data () {
      return {
        dialog: false,
        tabs: 0,
        tasks: {
          0: [
            {
              text: 'fuasdkjasnbfkjasbfkjhasbfijyhjbasf',
            },
            {
              text: 'fuasdkjasnbfkjasbfkjhasbfijyhjbasf',
            },
            {
              text: 'fuasdkjasnbfkjasbfkjhasbfijyhjbasf',
            },
            {
              text: 'fuasdkjasnbfkjasbfkjhasbfijyhjbasf',
            },
          ],
          1: [
            {
              text: 'fuasdkjasnbfkjasbfkjhasbfijyhjbasf',
            },
            {
              text: 'fuasdkjasnbfkjasbfkjhasbfijyhjbasf',
              value: false,
            },
          ],
          2: [
            {
              text: 'fuasdkjasnbfkjasbfkjhasbfijyhjbasf',
              value: false,
            },
            {
              text: 'fuasdkjasnbfkjasbfkjhasbfijyhjbasf',
              value: true,
            },
            {
              text: 'fuasdkjasnbfkjasbfkjhasbfijyhjbasf',
              value: true,
            },
          ],
        },
        list: {
          0: false,
          1: false,
          2: false,
        },
      }
    },

    methods: {
      complete (index) {
        this.list[index] = !this.list[index]
      },
    },
  }
</script>
