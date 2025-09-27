<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
    <ArtworkCard
      v-for="artwork in artworks"
      :key="artwork.id"
      :artwork="artwork"
      @click="$emit('artwork-click', artwork)"
    />
  </div>
</template>

<script setup lang="ts">
import ArtworkCard from './ArtworkCard.vue'
import type { Artwork } from '../types/api'

defineProps<{
  artworks: Artwork[]
}>()

defineEmits<{
  'artwork-click': [artwork: Artwork]
}>()
</script>

