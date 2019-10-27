<template>
<div id="main">
  <div v-if="no_login" class="loginbutton">
       <h1>为了方便你的信息统计，需要登录才能进行相关操作哦</h1>
       <button open-type="getUserInfo" @getuserinfo="bindGetUserInfo">点击登录</button>
  </div>
  <div v-else>
    <!-- <p>成功登录</p> -->
    <div id="user_info">
    <img :src="user_img" alt="">
    <p class="nick">{{ user_nickname }}</p>
      <div v-if="no_join" class="to_join">
        <p><span><button @click="Input_info_to_db">点击此处</button></span><span>确认加入我们或者获取你的环保信息</span></p> 
      </div>
      <div v-else class="action">
            <div class="huanbao">
              <p>总投入：{{ user_touru }}</p>
              <p>你的环保头衔：{{ user_touxian }}</p>
              <p>你已经成为一名优秀的环保爱好者!感谢你对我们活动的支持^_^</p>
            </div>
          <!-- 管理员的请求二维码权限 -->
          <div v-if="user_type==2">
            <button @click="ToGetPage">请求一个二维码</button>
            <button @click="ToSeeyuyue">点击查看本周预约</button>
          </div>       
          <div class="button_any">

              <li><mp-button type="primary" size="normal" btnClass="mb15" @click="To_touru">我要投入</mp-button></li>
              <li><mp-button type="primary" size="normal" btnClass="mb15" @click="To_yuyue">我要预约</mp-button></li>
              
            </div>
      </div>
    </div>
    
  </div>
</div>   
</template>
<style>
.loginbutton{
  padding:100px;
}
.loginbutton>h1{
  text-align: center
}
#user_info{
  border: 1px solid #23a9f2;
  margin-top:50px;
  margin-left: 5px;
  margin-right: 5px;
  border-radius: 5px;
  padding: 20px;
}
.nick{
  float: left;
  padding-left: 30px;
  padding-top: 20px;
  font-size: 25px;
  font-family: 'KaiTi_GB2312' 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}
.to_join{
  clear: both;
}
.action{
  clear: both;

}
.huanbao{
  clear: both;
  border: 5px solid #fffbe5;
  border-radius: 10px;
  box-shadow: 10px 5px #bacf98; 
  margin: 20px 0px 20px 0px;
}
/* 投入和预约 */
.button_any{
  padding-left: 20px;
  margin-left: 20px;
}
.button_any>li{
  float: left;
  margin-left: 20px;
  margin-top: 30px;
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
      token:'',
      user_type:1
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
          user_nickname : _this.user_nickname,
          user_img :_this.user_img
        },
        method: 'POST', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        header: {
          'content-type': 'application/x-www-form-urlencoded',
        }, // 设置请求的 header
        success: function(res){
          _this.no_join = false
          console.log(res)
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
        url: 'http://127.0.0.1:8000/api/auth/',
        data: {
          open_id:_this.user_openid
        },
        method: "POST", // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        }, // 设置请求的 header
        success: function(res){
          console.log(res.data)
          _this.token = res.data.token
          _this.user_type = res.data.user_type
          _this.user_touru = res.data.all_touru
          _this.user_touxian = res.data.level
          //成功之后直接将token写入缓存
          wx.setStorage({
            key: 'token',
            data: _this.token,
            success: function(res){
            //  console.log(res)
              console.log("token已经写入缓存中")
              // console.log("写入的是："+_this.token)
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
    },
    To_touru:function(){
      wx.navigateTo({
        url: '../../pages/second/main',
        success: function(res){
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
    To_yuyue:function(){
      wx.navigateTo({
        url: '../../pages/yuyue/main',
        success: function(res){
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
    ToSeeyuyue:function(){
      wx.navigateTo({
        url: '../../pages/seeyuyue/main',
        success: function(res){
          // success
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
div#user_info>img{
  width:100px;
  height: 100px;
  float: left;
}
#test{
  width:100px;
  height:100px;
}

</style>
