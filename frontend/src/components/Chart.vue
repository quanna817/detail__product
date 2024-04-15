<template>
    <div>
      <canvas id="priceChart" width="800" height="400"></canvas>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Chart from 'chart.js/auto';

  
  export default {
    name: "PriceChart",
    data() {
      return {
        priceHistory: []
      };
    },
    mounted() {
      this.fetchPriceHistory();
    },
    
    methods: {
      fetchPriceHistory() {
        const productId = this.$route.params.productId;
        axios.get(`http://127.0.0.1:8000/products/${productId}/price_history`)
          .then(response => {
            this.priceHistory = response.data;
            this.renderChart();
          })
          .catch(error => {
            console.error('Error fetching price history:', error);
          });
      },
      renderChart() {
      const ctx = this.$refs.priceChart.getContext('2d');
      const prices = this.priceHistory.map(entry => entry.price);
      const timestamps = this.priceHistory.map(entry => new Date(entry.timestamp).toLocaleString());

      new Chart(ctx, {
        type: 'line',
        data: {
          labels: timestamps,
          datasets: [{
            label: 'Price History',
            data: prices,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }]
        },
        options: {
          scales: {
            x: {
              type: 'time',
              time: {
                unit: 'day' 
              }
            },
            y: {
              title: {
                display: true,
                text: 'Price'
              }
            }
          }
        }
      });
    }
    }
  };
  </script>
  
  <style scoped>
  /* Add custom styles for the chart if needed */
  </style>
  