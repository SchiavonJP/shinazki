<template>
  <div :class="css.appHeader">
    <a :class="css.logo" href="/">
      <img :src="img.pilot" alt="Pilot" /> Shinazki bro, respect
    </a>
    <div :class="css.controls">
      <button
        :class="{ [css.activeControlsBtn]: activeStage === 'playlist' }"
        @click="$emit('toggle-playlist')"
      >
        Playlist
      </button>
      <button>
        <a target="_blank" rel="noopener noreferrer" href="https://www.instagram.com/shinazki/">
          <unicon width="28" height="28" name="instagram" fill="#fff" />
        </a>
      </button>
  
      <button>
        <a target="_blank" rel="noopener noreferrer" href="https://www.youtube.com/channel/UCviaWfMfmM2nPskGQJ13g0A/videos">
          <unicon width="28" height="28" name="youtube" fill="#fff" />
        </a>
      </button>
      <button>
        <a target="_blank" rel="noopener noreferrer" href="https://soundcloud.com/shinazki">
          <img :src="img.soundcloud" alt="soundcloud" />
        </a>
      </button>
      <button>
        <a target="_blank" rel="noopener noreferrer" href="https://www.beatstars.com/shinazki">
          <img :src="img.beatstars" alt="beatstars" />
        </a>
        
      </button>
      <input
        v-model="manualUrlInput"
        autofocus
        :class="css.urlInput"
        type="url"
        placeholder="Paste URL(s)"
        @input.stop="handleManualUrlChange"
        @keyup.stop
        @paste.stop
      />
      <button
        style="visibility: hidden;"
        :class="{ [css.activeControlsBtn]: activeStage === 'help' }"
        @click="$emit('toggle-help')"
      >
        <unicon width="28" height="28" name="question-circle" fill="#fff" />
      </button>
    </div>
  </div>
</template>

<script>
import css from "./AppHeader.module.css";
import pilot from "@/assets/pilot.svg";
import beatstars from "@/assets/beatstars.svg";
import soundcloud from "@/assets/soundcloud.svg";
import { getYtVideoId, getYtUrls } from "@/utils/string";

export default {
  props: {
    activeStage: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      manualUrlInput: "",
      css,
      img: {
        soundcloud,
        beatstars,
        pilot,
      },
    };
  },
  created() {
    const urls = ["https://www.youtube.com/watch?v=UM4MIdnHGj0", "https://www.youtube.com/watch?v=Wqv8e0inYAs", "https://www.youtube.com/watch?v=UtHldOQDPOc", "https://www.youtube.com/watch?v=VxhN7eLTseM",
                  "https://www.youtube.com/watch?v=ZiI3ZVIFvZo", "https://www.youtube.com/watch?v=ORjj3ofORHI", "https://www.youtube.com/watch?v=3pRrXqC7itg", "https://www.youtube.com/watch?v=10keb253kGM",
                  "https://www.youtube.com/watch?v=527n60lhQVc", "https://www.youtube.com/watch?v=NDvt4R_swrU", "https://www.youtube.com/watch?v=2DKwt3uDMvY", "https://www.youtube.com/watch?v=-ko03ZQBy2c",
                  "https://www.youtube.com/watch?v=jzFoQ3A5ZSo", "https://www.youtube.com/watch?v=xvtsJ0p1sAw", "https://www.youtube.com/watch?v=0muqYE4cQ0M", "https://www.youtube.com/watch?v=K0lHElbTJmY",
                  "https://www.youtube.com/watch?v=IAcm38nX99k", "https://www.youtube.com/watch?v=LuBO1gy_SAA", "https://www.youtube.com/watch?v=REf6R1dMxRg", "https://www.youtube.com/watch?v=jBK6hfw5ZFo",
                  "https://www.youtube.com/watch?v=r0gpbaweX3s", "https://www.youtube.com/watch?v=p-LVm5PmMBA", "https://www.youtube.com/watch?v=isHhcI0czpM", "https://www.youtube.com/watch?v=nnCE88AMg6Y",
                  "https://www.youtube.com/watch?v=Nv4LnWlKptQ", "https://www.youtube.com/watch?v=ug_LfJoUkiU"]
    
    urls.map(element => {
      getYtUrls(element);
    });
      const videoIds = urls.map(getYtVideoId);
    if (videoIds.length) {
      this.$emit("addYtUrls", videoIds);
      this.manualUrlInput = "";
    }
  },
  methods: {
    handleManualUrlChange() {
      const ytUrls = getYtUrls(this.manualUrlInput);
      const videoIds = ytUrls.map(getYtVideoId);

      if (videoIds.length) {
        this.$emit("addYtUrls", videoIds);
        this.manualUrlInput = "";
      }
    },
  },
};
</script>
