<template>
    <div class="header">
      <div class="logo">
        <img src="logo.png" alt="Logo">
      </div>
      <div class="menu">
        <ul>
          <li><a href="#">Trang chủ</a></li>
          <li><a href="#">Danh mục</a></li>
          <li><a href="#">Blog</a></li>
        </ul>
      </div>
      <div class="search">
        <input type="text" placeholder="Dán link hoặc tìm sản phẩm">
        <button>Tìm kiếm</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Header-s',
    
  }
  </script>
  
  <style scoped>
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #dfcdcd;
    color: white;
    padding: 10px 20px;
  }
  
  .logo img {
    width: 100px; 
  }
  
  .menu ul {
    list-style-type: none;
    display: flex;
  }
  
  .menu ul li {
    margin-right: 20px;
  }
  
  .search input[type="text"] {
    padding: 5px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }
  
  .search button {
    padding: 5px 10px;
    border-radius: 5px;
    border: none;
    background-color: orange;
    color: white;
    cursor: pointer;
  }
  </style>
  