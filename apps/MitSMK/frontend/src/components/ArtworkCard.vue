<template>
  <div 
    class="artwork-card group"
    @click="$emit('click', artwork)"
  >
    <div class="aspect-square mb-3 overflow-hidden rounded-lg bg-gray-100">
      <img
        v-if="artwork.image_thumbnail"
        :src="artwork.image_thumbnail"
        :alt="artwork.title || 'Kunstværk'"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        @error="handleImageError"
      />
      <div
        v-else
        class="w-full h-full flex items-center justify-center text-gray-400"
      >
        <span>Intet billede</span>
      </div>
    </div>
    
    <div class="space-y-1">
      <h3 class="font-medium text-gray-900 line-clamp-2">
        {{ artwork.title || 'Uden titel' }}
      </h3>
      
      <div class="flex items-center justify-between text-sm text-gray-600">
        <span v-if="artwork.artist_name">{{ artwork.artist_name }}</span>
        <span v-if="artwork.year">{{ artwork.year }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Artwork } from '../types/api'

defineProps<{
  artwork: Artwork
}>()

defineEmits<{
  click: [artwork: Artwork]
}>()

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
  img.parentElement!.innerHTML = '<div class="w-full h-full flex items-center justify-center text-gray-400"><span>Intet billede</span></div>'
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

