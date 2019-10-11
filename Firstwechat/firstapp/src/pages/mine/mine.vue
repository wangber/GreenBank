<template>
<div id="main">
  <div v-if="no_login">
       <button open-type="getUserInfo" @getuserinfo="bindGetUserInfo">点击登录</button>
       <img id="test" src="data:image/jpg;base64,iVBORw0KGgoAAAANSUhEUgAAAQUAAAEFAQAAAADC7c88AAABaUlEQVR4nO2ZQW6DMBBF38SRyI7cgNwkR+lRwtHCTegNYFGJSIHfhUNUKpJ2BViav8LWW3yNbPgzmHiv2+4PAJxwwgknVidaizpBbwbVY10u7CMhIpMkXWltD1ZSSJKW95EQ0ccTlXdhQCW0ZrspsYyPNIl4Gdf3sVFiP11mtyColveRHBGkeBmzPl5PaVjDRwJEPGM3A6Ag+woy+LSlfaRD2KRLao/YMAW8S3pJmJkVHWBlZUeQreMjCaI1M4Nz/dg8q6Hf4Ql2VpLUZBqQruS6g3Qt1AVFdVtxuhXiZ8VUAyZJdYyyXrE5SVLz/AJk8YyND16xGWmiLgzAuc67IHHxir0gnrOL9oBJZXVqD733le+IcXYRW3JJTXYHlUv7SIjox2kYJqhOeYd8PvYPIh/fYyv72DLxa3ZBvxtE9VETxvZpK063Qox5TIrBFRMXz2Pv9MhjADyjfh3Xni5mZP6H1wknnEic+Abm+t9w7DtC0gAAAABJRU5ErkJggg==">
  </div>
  <div v-else>
    <p>成功登录</p>
    <div id="user_info">
    <img :src="user_img" alt="">
    <p>用户昵称：{{ user_nickname }}</p>
    <p>总投入：{{ user_touru }}</p>
    <p>你的环保头衔：{{ user_touxian }}</p>
      <div v-if="no_join">
        <button @click="Input_info_to_db">点击提供你的信息给我们</button>
      </div>
      <div v-else>
       <p>你的信息已经提供</p>
       <!-- <button @click="GetCode">请求一个二维码</button> -->
        <button @click="ToGetPage">请求一个二维码</button>
      </div>

    </div>
  </div>
  

</div>   
</template>
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
      //头像 昵称 投入总量,头衔
      user_img:'',
      user_nickname:'初始化昵称',
      user_touru:'',
      user_touxian:'',
      user_jscode: "",
      //用户标识
      no_login:true,
      no_join:true,
      user_openid:"默认id",
      token:''
    };
  },
  methods: {
    bindGetUserInfo: function() {
      let _this = this;
      wx.login({
        success: function(res) {
          _this.user_jscode = res.code;
          console.log("登录成功");
          wx.request({
            url: "https://api.weixin.qq.com/sns/jscode2session",
            data: {
              appid: "wx36c1cdf40194e860",
              secret: "061e1a2c2c4415fb07b1a13ca286e425",
              js_code: _this.user_jscode,
              grant_type: "authorization_code"
            },
            method: "GET", // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
            //header: {}, // 设置请求的 header
            success: function(res) {
              console.log("请求结果");
              // console.log(res);
              _this.user_openid = res.data.openid
              _this.no_login=false;
              // success
            },
            fail: function() {
              // fail
            },
            complete: function() {
              // complete
            }
          });
        },
        fail: function() {
          console.log("登录失败");
          // fail
        },
        complete: function() {
          console.log("登录结束");
          // complete
        }
      });
      wx.getUserInfo({
        success: function(res) {
          console.log("获得用户信息");
          _this.user_img = res.userInfo.avatarUrl
          _this.user_nickname = res.userInfo.nickName
          // success
        },
        fail: function() {
          // fail
        },
        complete: function() {
          // complete
        },
      });  
    },

    Input_info_to_db:function(){
      let _this = this;
      wx.request({
        url: 'http://127.0.0.1:8000/api/login_up/',
        data: {
          
          user_openid : _this.user_openid,
          user_nickname : _this.user_nickname
        },
        method: 'POST', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        header: {
          'content-type': 'application/x-www-form-urlencoded',
        }, // 设置请求的 header
        success: function(res){
          _this.no_join = false
          // console.log(res)
        },
        fail: function() {
          console.log("写入失败")
        },
        complete: function() {
          // complete
        }
      });
      //认证——获取token
      wx.request({
        url: 'http://127.0.0.1:8000/apitest/auth',
        data: {
          open_id:_this.user_openid
        },
        method: "POST", // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        }, // 设置请求的 header
        success: function(res){
          _this.token = res.data.token
          //成功之后直接将token写入缓存
          wx.setStorage({
            key: 'token',
            data: _this.token,
            success: function(res){
              console.log(res)
              console.log("token已经写入缓存中")
              console.log("写入的是："+_this.token)
          // success
            },
            fail: function() {
              console.log("缓存写入失败")
            },
            complete: function() {
              // complete
            }
          });
          // console.log(res)
          // console.log(_this.token)
          // success
        },
        fail: function() {
          // fail
        },
        complete: function() {
          // complete
        }
      });
      //设置缓存
      
      wx.getStorage({
        key: 'token',
        success: function(res){
          console.log(res)
        },
        fail: function() {
          // fail
        },
        complete: function() {
          // complete
        }
      }) 
    },

    
    ToGetPage:function(){
      let _this = this
      wx.navigateTo({
        url: '../../pages/get-QR/main?token='+_this.token,
        success: function(res){
          console.log("已经前往获取二维码页面")
          // console.log(res)
          // success
        },
        fail: function() {
          console.log("跳转失败")
          // fail
        },
        complete: function() {
          console.log("跳转了吗？")
          // complete
        }
      })
    }
  }
};
</script>

<style>
div#user_info>img{
  width:100px;
  height: 100px;
}
#test{
  width:100px;
  height:100px;
}
</style>
