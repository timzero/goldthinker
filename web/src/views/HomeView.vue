<script setup lang="ts">
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <main>
    <div id="container">
      <form id="store-form" class="info bg-gray-700 bg-opacity-70 shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <textarea type="text" placeholder="Tell me something" id="itemToStore" class="overflow-auto resize-y form-input mb-4 shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline placeholder-gray-300" v-model="itemToStore" />
        <div class="flex items-center mt-2">
          <button id="store-button" :disabled="loading || !itemToStore" class="bg-yellow-500 mr-3 text-black font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" @click="tell">Tell</button>
        </div>
      </form>
      <form id="search-form" class="info bg-gray-700 bg-opacity-70 shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <textarea type="text" placeholder="Ask me a question" id="query" class="overflow-auto resize-y form-input mb-4 shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline placeholder-gray-300" v-model="query" />
        <div class="flex items-center mt-2">
          <button id="search-button" :disabled="loading || !query" class="bg-yellow-500 mr-3 text-black font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" @click="ask">Ask</button>
        </div>
      </form>
      <CircleProgressBar v-if="loading" class="progress" :max="100" >{{  }}</CircleProgressBar>
    </div>
    <div class="info bg-gray-700 bg-opacity-70 shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <ul>
        <li v-for="answer in answers" :key="answer.question">
          <div class="mt-2 text-left">
            <p class="text-green-300 text-base ">{{ answer.question }}</p>
          </div>
          <div class="mt-2 text-right">
            <p class="text-blue-300 text-base ">{{ answer.answer }}</p>
          </div>
        </li>
      </ul>
    </div>
  </main>
</template>

<script lang="ts">
  import logo from '/src/assets/logo.png';

  export default {

    mounted() {
    },
    data() {
      return {
        showMobileNav: false,
        showSignIn: false,
        logo: logo,
        itemToStore: '',
        query: '',
        loading: false,
        questions: [],
        answers: [],
      }
    },
    computed: {
      mobileNavClass() {
        return this.showMobileNav ? '' : 'hidden lg:block'
      },
    },
    methods: {
      toggleMobileNav() {
        this.showMobileNav = !this.showMobileNav;
      },
      hideMobileNav() {
        this.showMobileNav = false;
      },
      tell() {
        this.loading = true;
        const url = "http://localhost:5000/tell";
        const options = {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json;charset=UTF-8",
          },
          body: JSON.stringify({
              "text": this.itemToStore,
          }),
        };

        fetch(url, options)
        .then((response) => {
          return response.json()
        }, (error) => {
          console.log(error);
          this.loading = false;
        })
        .then((data) => {
          console.log(data);
          if(data.error) {
            console.log(data.error);
            this.loading = false;
          } else {
            this.loading = false;
            this.itemToStore = '';
          }
        });
      },
      ask() {
        this.loading = true;
        const url = "http://localhost:5000/ask";
        const options = {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json;charset=UTF-8",
          },
          body: JSON.stringify({
              "query": this.query,
          }),
        };

        fetch(url, options)
        .then((response) => {
          return response.json()
        }, (error) => {
          console.log(error);
          this.loading = false;
        })
        .then((data) => {
          console.log(data);
          if(data.error) {
            console.log(data.error);
            this.loading = false;
          } else {
            this.loading = false;
            this.answers.push({
              'question': this.query,
              'answer': data
            });
            this.playAudio(data);
          }
        });
      },
      playAudio(text) {
        const url = "http://localhost:5000/tts";
        const options = {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json;charset=UTF-8",
          },
          body: JSON.stringify({
              "text": text,
          }),
        };

        const ctx = new AudioContext();
        let audio;
        fetch(url, options)
        .then(data => data.arrayBuffer(), (error) => {
          console.log(error);
        })
        .then(arrayBuffer => ctx.decodeAudioData(arrayBuffer))
        .then(decodedAudio => {
          audio = decodedAudio;
          const playSound = ctx.createBufferSource();
          playSound.buffer = audio;
          playSound.connect(ctx.destination);
          playSound.start(ctx.currentTime);
        })
      }
    }
  }

</script>
