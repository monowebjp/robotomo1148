<template>
  <nav>
    <ul>
      <li :class="{ current: isCurrentRoute('/') }"><nuxt-link to="/">HOME</nuxt-link></li>
      <li :class="{ current: isCurrentRoute('/profile') }"><nuxt-link to="/profile">PROFILE</nuxt-link></li>
      <li :class="{ current: isCurrentRoute('/note') }"><nuxt-link to="/note">NOTE</nuxt-link></li>
      <li :class="{ current: isCurrentRoute('/thanks') }"><nuxt-link to="/thanks">THANKS</nuxt-link></li>
      <li :class="{ current: isCurrentRoute('/tools') }"><nuxt-link to="/tools">TOOLS</nuxt-link></li>
    </ul>
  </nav>
</template>

<script lang="ts">
export default {
  methods: {
    isCurrentRoute(routePath) {
      if (routePath === '/') {
        return this.$route.path === '/'
      }
      return this.$route.path.startsWith(routePath)
    }
  }
}
</script>

<style lang="scss" scoped>
ul, li {
  margin: 0;
  padding: 0;
}

ul {
  display: flex;
  justify-content: space-between;
}

li {
  list-style: none;
  font-weight: 700;
  margin-left: 40px;
  letter-spacing: 1.5px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, .7), -1px -1px 2px rgba(0, 0, 0, .5);

  &.current {
    text-shadow: none;

    > a {
      color: $font-color;

      &::before {
        width: 100%;
      }
    }
  }

  &:hover {
    > a {
      &::after {
        width: 100%;
      }
    }
  }
}

a {
  position: relative;
  padding: 3px 9px 3px 10.5px;
  display: block;
  color: $white;
  text-decoration: none;
  transition: color .15s ease-out, text-shadow .15s ease-out;

  &::before,
  &::after {
    position: absolute;
    bottom: 0;
    left: 50%;
    z-index: -1;
    transform: translateX(-50%);
    content: "";
    display: block;
    background: $white;
    width: 0;
    border-radius: 2px;
    transition: width .15s ease-out;
  }

  &::before {
    height: 100%;
  }

  &::after {
    height: 2px;
  }
}
</style>