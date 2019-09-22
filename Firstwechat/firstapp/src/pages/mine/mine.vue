<template>
<div id="main">
  <button open-type="getUserInfo" @getuserinfo="bindGetUserInfo">点击登录</button>
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
      user_jscode: "",
      has_login:false,
      //头像 昵称 投入总量,头衔
      user_img:'',
      user_nickname:'',
      user_touru:'',
      user_touxian:''
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
            // header: {}, // 设置请求的 header
            success: function(res) {
              console.log("请求结果");
              console.log(res);
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
          console.log(res);

          // success
        },
        fail: function() {
          // fail
        },
        complete: function() {
          // complete
        }
      });
    }
  }
};
</script>

<style>
</style>
