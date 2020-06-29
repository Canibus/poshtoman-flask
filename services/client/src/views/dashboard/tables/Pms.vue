<template>
  <v-container
    id="regular-tables"
    fluid
    tag="section"
  >
    <v-data-table
      :headers="headers"
      :items="items"
    >
      <template v-slot:top>
        <v-toolbar
          flat
          color="green"
        >
          <v-toolbar-title>Список устройств</v-toolbar-title>
          <v-divider
            class="mx-4"
            inset
            vertical
          />
          <v-spacer />
          <v-dialog
            v-model="dialog"
            max-width="800px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="blue"
                dark
                class="mb-2"
                v-bind="attrs"
                v-on="on"
              >
                Новое устройство
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="headline">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.factory_num"
                        label="Заводской номер"
                      />
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.numbox"
                        label="Номер"
                      />
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.url"
                        label="URL адрес"
                      />
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.address"
                        label="Адресс"
                      />
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.comment"
                        label="Комментарий"
                      />
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-select
                        v-model="place"
                        :items="places"
                        item-text="address"
                        item-value="id"
                        label="Выберите"
                        persistent-hint
                        return-object
                        single-line
                    ></v-select>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer />
                <v-btn
                  color="blue darken-1"
                  text
                  @click="close"
                >
                  Отменить
                </v-btn>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="save"
                >
                  Сохранить
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon
          small
          class="mr-2"
          @click="editItem(item)"
        >
          mdi-pencil
        </v-icon>
        <v-icon
          small
          @click="deleteItem(item)"
        >
          mdi-delete
        </v-icon>
      </template>
      <template v-slot:no-data>
        <v-btn
          color="primary"
          @click="initialize"
        >
          Reset
        </v-btn>
      </template>
    </v-data-table>
  </v-container>
</template>
<script>
  import axios from 'axios'
  import config from './config'
  export default {
    data () {
      return {
        editedIndex: -1,
        dialog: false,
        place: {},
        headers: [
          {
            text: 'ID',
            value: 'id',
          },
          {
            text: 'Завод.№',
            value: 'factory_num',
          },
          {
            text: 'Номер',
            value: 'numbox',
          },
          {
            text: 'Темп.зона',
            value: 'numbox',
          },
          {
            text: 'URL',
            value: 'url',
          },
          {
            text: 'Адрес',
            value: 'address',
          },
          {
            text: 'Комментарий',
            value: 'comment',
          },
          {
            text: 'Расположение',
            value: 'place_id',
          },
          {
            text: 'Ячейки',
            value: 'cells',

          },
          {
            text: 'Действия',
            value: 'actions',
            sortable: false,
          },
        ],
        items: [],
        places: [],
        editedItem: {
          factory_num: '',
          numbox: '',
          url: '',
          address: '',
          comment: '',
          place_id: '',
          cells: [],
        },
        defaultItem: {
          factory_num: '',
          numbox: '',
          url: '',
          address: '',
          comment: '',
          place_id: '',
          cells: [],
        },
      }
    },
    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'Добавление' : 'Редактирование'
      },
    },

    watch: {
      dialog (val) {
        val || this.close()
      },
    },

    created () {
      this.initialize()
    },

    methods: {
      initialize () {
        axios({ url: `${config.apiUrl}/api/v2/pm/`, method: 'GET' })
          .then(response => {
            this.items = response.data
          })
        axios({ url: `${config.apiUrl}/api/v2/places/`, method: 'GET' })
          .then(response => {
            this.places = response.data
          })
      },

      editItem (item) {
        this.editedIndex = this.items.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        const index = this.items.indexOf(item)
        confirm('Вы действительно хотите удалить это устройство?')
        axios({ url: `${config.apiUrl}/api/v2/pm/` + this.items[index].id, method: 'DELETE' })
          .then(response => {
            if (response.status === 204) {
              this.items.splice(index, 1)
            }
          })
      },

      save () {
        this.editedItem.place_id = this.place.id
        if (this.editedIndex > -1) {
          axios({ url: `${config.apiUrl}/api/v2/pm/` + this.items[this.editedIndex].id, data: this.editedItem, method: 'PUT' })
            .then(response => {
              if (response.status === 200) {
                this.items[this.editedIndex] = response.data
              }
            })
        } else {
          axios({ url: `${config.apiUrl}/api/v2/pm/`, data: this.editedItem, method: 'POST' })
            .then(response => {
              if (response.status === 200) {
                this.items.push(this.editedItem)
              }
            })
        }
        this.close()
        this.initialize()
      },

      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },
    },
  }
</script>
