<template>
  <div id="app">
    <div v-if="product" class="product-container">
      <div class="left-section">
        <div class="image-container">
          <img :src="mainImage" alt="Main Image" :style="{ width: '550px', height: '550px' }" @click="showLargeImage(mainImage)">
          <div class="thumbnail-container">
            <img v-for="image in product.images" :key="image.id" :src="image.url" alt="Product Image" :style="{ width: '100px', height: '100px', margin: '5px', cursor: 'pointer' }" @click="showLargeImage(image.url)">
          </div>
        </div>
      </div>
      <div class="right-section">
        <div class="product-info">
          <h2>{{ product.name }}</h2>
          <p>Description: {{ product.description }}</p>
          <p>Price: {{ product.price }}</p>
        </div>
      </div>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      product: null,
      mainImage: '',
    };
  },
  mounted() {
    this.fetchProduct();
  },
  methods: {
    async fetchProduct() {
      const productId = this.$route.params.productId;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/products/${productId}`);
        this.product = response.data;
        this.mainImage = this.product.images[0].url; 
      } catch (error) {
        console.error('Error fetching product:', error);
      }
    },
    showLargeImage(url) {
      this.mainImage = url;
    },
  },
};
</script>

<style>
.product-container {
  display: flex;
  justify-content: center;
}

.left-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.right-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.image-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.thumbnail-container {
  display: flex;
}

.product-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>