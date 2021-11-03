<template>
  <div
    :class="css.editor"
    @drag.stop
    @dragstart.stop
    @dragend.stop
    @dragexit.stop
    @dragover.stop
    @drop.stop
    @dragenter.stop
    @dragleave.stop
  >
    <header :class="css.header">
      <h3>
        <span v-if="!loading">Playlist – {{ songNumber }} videos</span>
        <span v-else>loading videos...</span>
      </h3>
      <div v-if="songNumber" :class="css.playlistControls">
        <button @click="$emit('shuffle')">
          <unicon width="26" height="26" name="shuffle" fill="#4a635d" />
        </button>
        <button style="visibility: hidden;" @click="$emit('clearPlaylist')">
          <unicon width="26" height="26" name="trash" fill="#4a635d" />
        </button>

        <button style="visibility: hidden;" :class="css.textButton" @click="$emit('generatePlaylistURL')">
          Create Playlist URL to share
        </button>
      </div>
    </header>

    <div v-if="playlistCopy && playlistCopy.length">
      <draggable
        tag="ul"
        class="list-group"
        :animation="150"
        :handle="`.${css.dragHandle}`"
        :list="playlistCopy"
        :ghost-class="css.songUrlGhost"
        @update="onUpdate"
      >
        <li
          v-for="(song, i) in playlistCopy"
          :key="song.videoId"
          :class="[css.songUrl, { [css.activeSongUrl]: i === playlistIndex }]"
          @click="$emit('selectedSongIndex', i)"
        >
          <span :class="css.dragHandle">
            <unicon :class="css.dragHandleIcon" name="draggabledots" />
            <span :class="css.dragHandleIndex">{{ i + 1 }}</span>
          </span>
          <span
            v-if="songInfo[song.videoId]"
            :class="css.songThumb"
            :style="songThumbStyle(songInfo[song.videoId])"
          />
          <span v-if="songInfo[song.videoId]" :class="css.songTitle">
            {{ createTextElipsis(songInfo[song.videoId].title) }}
          </span>
          <span v-else :class="css.songTitle">{{ songName[i] }}</span>
        </li>
      </draggable>
    </div>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import css from "./SongList.module.css";

export default {
  props: {
    playlist: {
      type: Array,
      validator: (list) =>
        list.reduce((isPlaylist, song) => {
          if (!isPlaylist) return isPlaylist;

          return !!song.videoId;
        }, true),
    },

    playlistIndex: {
      type: Number,
    },
  },

  components: {
    draggable,
  },

  data() {
    return {
      css,
      songName: ['[FREE] Hard/Dark Type Beat 2021 - "Session" (prod. Shinazki)', '[FREE] Boom Bap Type Beat 2021 - "Wisdom" (prod. Shinazki)', '[FREE] Melancholic Type Beat 2021 - "Empty" (prod. Shinazki)',
                '[FREE] Melodic Type Beat 2021 - "Neverland" (prod. Shinazki)', '[FREE] Melodic Mood Type Beat 2021 - "Strangers" (prod. Shinazki)', '[FREE] Melancholic Type Beat 2021 - "Happy Thoughts" (prod. Shinazki)',
                '[FREE] Melodic Retro Type Beat 2021 - "Golden" (prod. Shinazki)', '[FREE] Boom Bap Melodic Type Beat 2021 - "K7DAGLH" (prod. Shinazki)', '[FREE] Chill Melodic Type Beat 2021 - "Dusk" (prod. Shinazki)',
                '[FREE] Brazilian Funk Type Beat 2021 - "Big Prom" (prod. Shinazki)', '[free] chill hop lofi type beat 2021 - "daydream" (prod. shinazki)', '[FREE] Hyperpop x EDM x Trap Type Beat 2021 - "XXXXXX" (prod. Shinazki)',
                '[FREE] Melodic Guitar Type Beat 2021 - "Wild Wild West" (prod. Shinazki)', '[FREE] Melodic Guitar Type Beat 2021 - "Riot" (prod. Shinazki)', '[FREE] Phonky Type Beat 2021 - "DK" (prod. Shinazki)',
                '[FREE] Twenty One Pilots Type Beat 2021 - "Voices" (prod. Shinazki)', '[FREE] Twenty One Pilots Type Beat 2021 - "Adored" (prod. Shinazki)', 'shinazki - Despicable', '[FREE] Drum & Bass Type Beat 2021 - "Blur" (prod. Shinazki)',
                '[FREE] Synthwave Type Beat 2021 - "Neotokyo" (prod. Shinazki)', '[FREE] EDM Trap Type Beat 2021 - "Under The Hoodie" (prod. Shinazki)', '[FREE] EDM House Type Beat 2021 - "Focus" (prod. Shinazki)', 'shinazki - dog days',
                '[FREE] Orchestral Jungle Type Beat 2021 - "Doomsday" (prod. Shinazki)', '[FREE] Chill Lofi Type Beat 2021 - "Dawn" (prod. Shinazki)', "gumball but it's lofi and kind of sad"],
      songInfo: {},
      loading: false,
      playlistCopy: [],
    };
  },

  computed: {
    songNumber() {
      return this.playlistCopy.length;
    },
  },


  methods: {
    async fetchSongInfo() {
      if (!this.playlistCopy.length) return;

      this.loading = true;
      const videoIds = this.playlistCopy.map((video) => video.videoId);

      this.$http
        .fetchOembedBatch(videoIds)
        .then((response) => {
          const videos = response.videos || [];
          const failedVideos = response.failed || [];

          failedVideos.forEach((fail) => {
            this.$emit("videoInfoError", fail.videoId);
          });

          if (failedVideos.length) {
            this.$notify({
              text: `Unfortunately, some videos couldn't load. It may be because of geographic restrictions, video settings or the video doesn't exist anymore. Please try to use another link.`,
              type: "error",
              duration: 12000,
            });
          }

          videos.forEach((oembed) => {
            this.$set(this.songInfo, oembed.videoId, oembed.video);
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },

    createTextElipsis(text) {
      return this.$utils.string.textElipsis(text, 60);
    },

    songThumbStyle(songInfo) {
      return {
        backgroundImage: `url(${songInfo.thumbUrl})`,
      };
    },

    onUpdate(evt) {
      evt; // skip compiler error for unused var
      // console.log(evt);
      this.$emit("playlistOrderChange", this.playlistCopy);
    },
  },

  watch: {
    playlist() {
      this.playlistCopy = [...this.playlist];
      this.fetchSongInfo();
    },
  },
};
</script>
