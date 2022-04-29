<template>
  <!-- <v-for a_frame><iframe src= a_frame[k] ...</v-for> -->
  <iframe
    :key="trigger_update_url"
    :src="view_url"
    frameborder="0" width="100%" height="100%">
  </iframe>
</template>

<script>
  let my_url;
  export default {
    name: "analysis",
    data() {
      return {
        view_url: ''
      }
    },
    computed: {
      trigger_update_url() {
        this.view_url = "about:blank";
        this.change_url()
        return this.$route.meta.url;
      }
    },
    methods: {
      read_from_router() {
        // console.log(this.$route.meta.url);
        return this.$route.meta.url;
      },
      async change_url() {
        let url = this.read_from_router();
        let end = url.indexOf("?");
        // console.log(end);
        let content_url = url.substring(7, end);
        // console.log(content_url);
        let username = sessionStorage.getItem('tableau_backend_username');
        // console.log(username);
        let auth = await (await fetch('http://10.94.81.132:5000/logic.check_view?username=' + username + '&content_url=' + content_url)).json();
        // console.log(auth.view);
        if (auth.view) {
          let userid = sessionStorage.getItem('tableau_backend_userid');
          // console.log(userid);
          let token_o = await (await fetch('http://10.94.81.132:5000/get_token?userid=' + userid)).json();
          if (token_o) {
            //old(need login with cookie save): url = "http://10.94.81.132/views/_0/sheet0?:showAppBanner=false&:origin=viz_share_link&:display_count=n&:showVizHome=n",
            //e.g. http://10.94.81.132/trusted/TqzPvNviQKSIw4aoHpDI-Q==:AUj8fPbWaUnXnupipU60baIf/views/_0/sheet0?:showVizHome=no&:embed=true&:showShareOptions=false&:toolbar=top&:tabs=no

            my_url = `${token_o.url}/trusted/${token_o.token}${url}`;
            // console.log(token_o.url);
            this.view_url = my_url;

            // console.log("111", token_o);
          } else {
            //TODO sess expired?
            // console.log("222", token_o);
          }
          // return my_url;
        }
        else {
          this.view_url = 'http://10.94.81.132:8080/403';
        }
      }
    },
    async mounted() {
    }
  }
</script>

<style scoped>

</style>
