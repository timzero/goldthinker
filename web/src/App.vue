

<template>
  <div>
    <header>
      <div class="wrapper">     
        <nav class="flex items-center justify-between flex-wrap p-6" :class="{'is-home': $route.name === 'home', 'open': showMobileNav}">
          <div class="flex items-center flex-shrink-0 text-white mr-6">
            <a href="/" @click="hideMobileNav"><img :src="logo" class="h-16 w-16" /></a>
            <span class="text-3xl font-bold tracking-wide py-2 pl-1 uppercase font-serif">Goldthinker</span>
          </div>
          <div class="block lg:hidden">
            <button class="flex items-center px-3 py-2 border rounded text-yellow-400 border-yellow-400 hover:text-white hover:border-white" @click="toggleMobileNav">
              <svg class="fill-current h-3 w-3" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><title>Menu</title><path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"/></svg>
            </button>
          </div>
          <div :class="`w-full block flex-grow lg:flex lg:items-center lg:w-auto ${mobileNavClass}`">
            <div class="text-sm lg:flex-grow text-right">
              <a  @click="hideMobileNav" class="block mt-4 lg:inline-block lg:mt-0 text-yellow-400 hover:text-white mr-4" href="/about">About</a>
            </div>
            
          </div>
        </nav>
      </div>
    </header>

    <RouterView />
  </div>
</template>

<script lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import logo from '/src/assets/logo.png';

export default {

  mounted() {
  },
  data() {
    return {
      showMobileNav: false,
      showSignIn: false,
      logo: logo,
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
  }
}

</script>


<style scoped lang="scss">
.header {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 100;
  width: 100%;
}

body {
  background-color: b0b0af;
}

button[type='submit'] {
  background-color: var(--amplify-components-button-primary-background-color);
}

#app {
  position: absolute;
  top: 0;
}

.background-black {
  background-color: black;

  &.is-home {
    background-color: transparent;
  
    &.open {
      @apply mb-4;
    }
  }
}
</style>
