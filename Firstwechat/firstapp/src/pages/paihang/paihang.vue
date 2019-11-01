<template>
<div id="main">
  <div v-if="no_get">
    <button @click="Getform">点击查看排行榜</button>
  </div>
  <div v-else>
    <h1>累计贡献排行榜</h1>
    <p>更新时间：{{time}}</p>
    <!-- 实现滑动 -->
          <!-- <scroll-view class='scroll-view-list-vertical' scroll-y="true">
            <div class="scroll-view-item-vertical" :key="key" v-for="(idx, key) in iconMap">
              <img :src="iconImg" alt="" :style="{background: iconMap[key]['bk']}">
              <span>{{iconMap[key]['title']}}</span>
            </div>
          </scroll-view>  -->
    <!-- 实现滑动 -->
          <div class="usertext">           
          </div>
          <scroll-view class='scroll-view-list-vertical' scroll-y="true">
            <div class="scroll-view-item-vertical" v-for="(key,idx) in alluser">
              <!-- <img :src="iconImg" alt="图片未加载" :style="{background:#8B67E5}"> -->
              <img :src=key.user_img alt="">
              <div class="usertext">
                <span>{{key.nickname}}</span><span>{{key.all_touru}}</span><span>{{key.level}}</span>
              </div>
            
            </div>
          </scroll-view> 
  </div>
  
</div>   
</template>
<style>
h1{
  text-align: center;
  font-size: 30px;
  border-radius: 10px;
  background-image:linear-gradient(120deg, #d4fc79 0%, #96e6a1 100%);
  margin: 20px;
}
.one_user{
      padding-left:20px;
      margin-left: 20px
}
.scroll-view-list-vertical {
    height: 400px;
    margin-top: 20px;
    }

.scroll-view-item-vertical {                
        height: 50px;
        margin: 20px 20px;
        border: 2px solid #0085e2;
        background: #f9fdd5;
        border-radius: 5px;
        padding: 5px;
        }

img {
            border-radius: 50%;                
            width: 110rpx;
            height: 110rpx;        
            float: left;    
        }
span {                
            font-size: 20px;
            padding: 5px;    
        }

        
</style>
<script>
import mpInput from "mpvue-weui/src/input";
import mpModal from "mpvue-weui/src/modal";
import mpButton from "mpvue-weui/src/button";

export default {
  components: {
    mpButton,
    mpModal,
    mpInput
  },
  config:{
    enablePullDownRefresh:true
  },
  data() {
    return {
     alluser:'',
     no_get:true,
     user_img:'',
     time:''
    };
  },
  methods: {
    Getform:function(){
      let _this = this;
      wx.request({
        url: 'http://127.0.0.1:8000/api/paihang',
        data: {},
        method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        // header: {}, // 设置请求的 header
        success: function(res){
          // success
          _this.alluser = res.data.alluser
          _this.time = res.data.time
          console.log(_this.time)
          _this.no_get = false
        },
        fail: function() {
          // fail
        },
        complete: function() {
          // complete
        }
      })
    }
  }
};
</script>

<style>

</style>
