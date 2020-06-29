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
          <v-toolbar-title>Список мест</v-toolbar-title>
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
                Новое место
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
                        label="Название"
                      />
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.address"
                        label="Адрес"
                      />
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.org_name"
                        label="Организация"
                      />
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.bailee"
                        label="Ответственный"
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
                        v-model="editedItem.places"
                        :items="selectedPlaces"
                        label="Выберите почтоматы"
                        multiple
                      >
                      </v-select>
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
  export default {
    data () {
      return {
        editedIndex: -1,
        dialog: false,
        headers: [
          {
            text: 'ID',
            value: 'id',
          },
          {
            text: 'Название',
            value: 'name',
          },
          {
            text: 'Адрес',
            value: 'address',
          },
          {
            text: 'Организация',
            value: 'org_name',
          },
          {
            text: 'Ответственный',
            value: 'bailee',
          },
          {
            text: 'Телефон',
            value: 'phone',
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
          address: '',
          org_name: '',
          bailee: '',
          phone: '',
          comment: '',
          pms: [],
          cells: '',
        },
        defaultItem: {
          name: '',
          address: '',
          org_name: '',
          bailee: '',
          phone: '',
          comment: '',
          pms: [],
          cells: '',
        },
        selectedPlaces: ['Улица 1', 'Улица 2', 'Улица 3'],
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
        axios({ url: 'http://127.0.0.1:5000/api/v2/places/', method: 'GET' })
          .then(response => {
            this.items = response.data
          })
      },

      editItem (item) {
        this.editedIndex = this.items.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        const index = this.items.indexOf(item)
        confirm('Вы действительно хотите удалить это место?')
        axios({ url: 'http://127.0.0.1:5000/api/v2/places/' + this.items[index].id, method: 'DELETE' })
          .then(response => {
            if (response.status === 204) {
              this.items.splice(index, 1)
            }
          })
      },

      save () {
        if (this.editedIndex > -1) {
          axios({ url: 'http://127.0.0.1:5000/api/v2/places/' + this.items[this.editedIndex].id, data: this.editedItem, method: 'PUT' })
            .then(response => {
              if (response.status === 200) {
                this.items[this.editedIndex] = response.data
              }
            })
        } else {
          axios({ url: 'http://127.0.0.1:5000/api/v2/places/', data: this.editedItem, method: 'POST' })
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
    },
  }
</script>
