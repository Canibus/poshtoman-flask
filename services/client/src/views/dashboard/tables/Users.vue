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
          color="green"
        >
          <v-toolbar-title>Список клиентов</v-toolbar-title>
          <v-divider
            class="mx-4"
            inset
            vertical
          />
          <v-spacer />
          <v-dialog
            v-model="ordersDialog"
            max-width="800px"
          >
            <template>
              <v-data-table
                :headers="ordersHead"
                :items="orders"
                :items-per-page="5"
                class="elevation-1"
              />
            </template>
          </v-dialog>
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
                Новый пользователь
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
                        v-model="editedItem.name"
                        label="Имя"
                      />
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.patronymic"
                        label="Отчевство"
                      />
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.surname"
                        label="Фамилия"
                      />
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.phone"
                        label="Телефон"
                      />
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-btn
                        color="green"
                        @click="sendSms(editedItem.phone)"
                      >
                        Отправить смс
                      </v-btn>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.email"
                        label="Email"
                      />
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.password"
                        label="Пароль"
                      />
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.keyword"
                        label="Ключевое слово"
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
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.sms"
                        label="Код-смс"
                      />
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
      <template v-slot:item.order="{ item }">
        <v-chip
          color="blue"
          dark
          @click="openOrders(item)"
        >
          {{ item.orders.length }}
        </v-chip>
      </template>
      <template v-slot:item.cell="{ item }">
        <v-chip
          color="yellow"
          @click="openOrders(item)"
        >
          {{ item.orders.length }}
        </v-chip>
      </template>
      <!-- <template v-slot:item.place>
        <v-chip
          color="orange"
          @click="openPlaces(item)"
        >
          {{ selectedPlaces.length }}
        </v-chip>
      </template> -->
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
  export default {
    data () {
      return {
        editedIndex: -1,
        dialog: false,
        ordersDialog: false,
        place: {},
        ordersHead: [
          {
            text: 'ID',
            value: 'id',
          },
          {
            text: 'Дата заказа',
            value: 'order_time',
          },
          {
            text: 'Курьер',
            value: 'courier_id',
          },
          {
            text: 'Почтомат',
            value: 'postmachine_id',
          },
          {
            text: 'Заказ взят',
            value: 'time_up',
          },
          {
            text: 'Заказ положен',
            value: 'time_down',
          },
          {
            text: 'Комментарий',
            value: 'comment',
          },
        ],
        headers: [
          {
            text: 'ID',
            value: 'id',
          },
          {
            text: 'Имя',
            value: 'name',
          },
          {
            text: 'Фамилия',
            value: 'surname',
          },
          {
            text: 'Отчевство',
            value: 'patronymic',
          },
          {
            text: 'Телефон',
            value: 'phone',
          },
          {
            text: 'Email',
            value: 'email',
          },
          {
            text: 'Слово',
            value: 'keyword',
          },
          {
            text: 'Заказы',
            value: 'order',
            sortable: false,
          },
          {
            text: 'Ячейки',
            value: 'cell',
          },
          {
            text: 'Места',
            value: 'place_id',
          },
          {
            text: 'Посл.актив.',
            value: 'last_activity',
          },
          {
            text: 'Комментарий',
            value: 'comment',
          },
          {
            text: 'Действия',
            value: 'actions',
            sortable: false,
          },
        ],
        items: [],
        orders: [],
        editedItem: {
          name: '',
          surname: '',
          patronymic: '',
          phone: '',
          email: '',
          password: '',
          keyword: '',
          comment: '',
          sms: '',
          place_id: '',
        },
        defaultItem: {
          name: '',
          surname: '',
          patronymic: '',
          phone: '',
          email: '',
          password: '',
          keyword: '',
          comment: '',
          sms: '',
          place_id: '',
        },
        places: [],
        id: null,
        name: null,
        surname: null,
        phone: null,
        email: null,
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
        axios({ url: 'http://127.0.0.1:5000/api/v2/clients/', method: 'GET' })
          .then(response => {
            this.items = response.data
          })
        axios({ url: 'http://127.0.0.1:5000/api/v2/places/', method: 'GET' })
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
        confirm('Вы действительно хотите удалить этого пользователя?')
        axios({ url: 'http://127.0.0.1:5000/api/v2/clients/' + this.items[index].id, method: 'DELETE' })
          .then(response => {
            if (response.status === 204) {
              this.items.splice(index, 1)
            }
          })
      },

      sendSms (phone) {
        axios({ url: 'http://127.0.0.1:5000/api/v2/clients/verify', data: { phone: phone }, method: 'POST' })
          .then(response => {
            if (response.status !== 204) {
              console.log(response.err)
            }
          })
      },

      save () {
        this.editedItem.place_id = this.place.id
        console.log(this.editedItem)
        if (this.editedIndex > -1) {
          axios({ url: 'http://127.0.0.1:5000/api/v2/clients/' + this.items[this.editedIndex].id, data: this.editedItem, method: 'PUT' })
            .then(response => {
              if (response.status === 200) {
                this.items[this.editedIndex] = response.data
              }
            })
        } else {
          axios({ url: 'http://127.0.0.1:5000/api/v2/clients/register', data: this.editedItem, method: 'POST' })
            .then(response => {
              if (response.status === 201) {
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

      openOrders (item) {
        const index = this.items.indexOf(item)
        this.orders = this.items[index].orders
        console.log(this.orders)
        this.ordersDialog = true
      },
    },
  }
</script>
