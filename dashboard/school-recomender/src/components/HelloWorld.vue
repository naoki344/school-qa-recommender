<template>
  <v-container>
    <v-item-group
      :mandatory="mandatory"
      :multiple="multiple"
    >
      <v-container class="pa-0">
        <v-row>
			<v-item class="col-md-4 col-12">
              <v-card
                v-if="type === 'cards'"
                :color="active ? 'light-green lighten-4' : ''"
                class="d-flex align-center"
                white
                height="200"
                @click="toggle"
              >
                <v-row justify="center">
                  <v-dialog v-model="dialog" persistent max-width="290">
                    <template v-slot:activator="{ on }">
                      <v-btn color="primary" dark v-on="on">Open Dialog</v-btn>
                    </template>
                    <v-card>
                      <v-card-title class="headline">Use Google's location service?</v-card-title>
                      <v-card-text>Let Google help apps determine location. This means sending anonymous location data to Google, even when no apps are running.</v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="green darken-1" text @click="dialog = false">Disagree</v-btn>
                        <v-btn color="green darken-1" text @click="dialog = false">Agree</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-row>
              </v-card>
			</v-item>
          <v-col
            v-for="n in 3"
            :key="n"
            cols="12"
            md="4"
          >
            <v-item v-slot:default="{ active, toggle }">
              <v-card
                v-if="type === 'cards'"
                :color="active ? 'light-green lighten-4' : ''"
                class="d-flex align-center"
                white
                height="200"
                @click="toggle"
              >
                <v-card-text>
                  <div>Word of the Day</div>
                  <p class="display-1 text--primary">
                    be•nev•o•lent
                  </p>
                  <p>adjective</p>
                  <div class="text--primary">
                    well meaning and kindly.<br>
                    "a benevolent smile"
                  </div>
                </v-card-text>
                <v-scroll-y-transition>
                  <div
                    v-if="active"
                    class="display-3 flex-grow-1 text-center font-weight-bold"
					color="light-green darken-4"
                  >
                    Add
                  </div>
                </v-scroll-y-transition>
              </v-card>
            </v-item>
          </v-col>
        </v-row>
      </v-container>
    </v-item-group>
  </v-container>
</template>

<script>
  import { VCard, VCardText } from 'vuetify/lib'
  export default {
    name: 'HelloWorld',
	components: {
      VCard,
      VCardText,
      // VCardActions,
    },
    data: () => ({
      types: [
        'cards',
        'images',
      ],
      type: 'cards',
      mandatory: false,
      multiple: true,
      dialog: false,
    }),
  }
</script>
