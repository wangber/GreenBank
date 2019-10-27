<template>
<div class="main">
    <div v-if="no_see">
        <button @click="See">点击查看预约</button>
    </div>
    <div class="list" v-else>
        <h1>预约情况</h1>
    <p>更新时间：{{old_time}}----{{new_time}}</p>
          <div class="usertext">          
          </div>
          <scroll-view class='scroll-view-list-vertical' scroll-y="true">
            <div class="scroll-view-item-vertical" v-for="(key,idx) in yuyuelist">
              <!-- <img :src="iconImg" alt="图片未加载" :style="{background:#8B67E5}"> -->
              <div class="yuyuetext">
                <span>{{key.location}}</span><span>{{key.yuyuetime}}</span>
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
  data() {
    return {
     old_time:'',
     new_time:'',
     yuyuelist:'',
     no_see:true
    };
  },
  methods: {
      See:function(){
          let _this = this
          wx.request({
              url: 'http://127.0.0.1:8000/api/seeyuyue',
              data: {},
              method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
              // header: {}, // 设置请求的 header
              success: function(res){
                  _this.no_see = false
                  _this.yuyuelist = res.data.ret_list
                  _this.old_time = res.data.old_time
                  _this.new_time = res.data.last_time
                  // success
              },
              fail: function() {
                  // fail
              },
              complete: function() {
                  // complete
              }
          })
      },
      back:function(){
      wx.switchTab({
        url: '/pages/index/main',
        success: function(res){
          console.log("跳转成功返回信息"+res)
          // success
        },
        fail: function() {
          console.log("跳转失败")
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
