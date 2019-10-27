<template>
<div>
  <div v-if="no_login">
    <p>你还未登录，前往“我的”页面去登录信息吧！</p>
  </div>
  <div v-else>
    <div>
     <h2>回收志愿者会提供专门的二维码扫描二维码既可以记录你的成绩</h2>
     </div>
    <div id="action">
     <button @click="touru()">点击扫码投入</button>
     </div>
     <div id="alert">
      <mp-modal ref="mpModal" :title="msg" :content="msg_2" :showCancel="false" @confirm="confirm"></mp-modal>
     </div>
  </div>
</div>

</template>
<style>
h2{
  font-size: 30px;
  text-align: center
}
</style>

<script>
import mpButton from "mpvue-weui/src/button";
import mpModal from "mpvue-weui/src/modal";
import mpInput from "mpvue-weui/src/input";
export default {
  components: {
    mpButton,
    mpModal,
    mpInput
  },
  data() {
    return {
      msg: "投入失败",
      msg_2: "对不起，投入失败，请使用有效的二维码重试或者尝试与管理人员联系",
      token:'',
      no_login:true,
      info:''
    };
  },

mounted() {
   this.onLoad();
  },

  methods: {
    
    onLoad:function(){
      let _this = this
      wx.getStorage({
        key: 'token',
        success: function(res){
          console.log("缓存获取情况")
          console.log(res)
          if (res.data != ""){
            _this.no_login = false
            console.log(res.data)
            _this.token = res.data
          }
          // success
        },
        fail: function() {
          console.log("缓存获取失败")
          // fail
        },
        complete: function() {
          // complete
        }
      })
    },

    back: function() {
      wx.navigateBack({
        delta: 1, // 回退前 delta(默认为1) 页面
        success: function(res) {
          console.log("投入成功");
          // success
        },
        fail: function() {
          // fail
          console.log("回退失败");
        },
        complete: function() {
          // complete
          console.log("回退完成");
        }
      });
    },
    touru: function() {
      console.log("点击按钮");
      let _this = this;
      //调用扫码并获取信息
      wx.scanCode({
        success(res) {
          // console.log(res);
          // console.log(res.result)
          _this.info = res.result
          //向链接发送请求
          wx.request({
            url: "http://127.0.0.1:8000/api/readcode/",
            data: {
                  info:_this.info,
                  token:_this.token
            },
            method: "POST", // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
            header: {'content-type': 'application/x-www-form-urlencoded',}, // 设置请求的 header
            success: function(res) {
              // success
              console.log("已经向二维码地址发送请求");
              console.log(res.data);
              //跳转到成功页面
              if (res.data.info == true){
                wx.navigateTo({
                            url: '../msg/main'
                          })
              }
              else{
                _this.$refs.mpModal.show();
              }
              
            },
            fail: function() {
              // fail
              console.log("成绩录入失败");
              //跳转到失败页面
              _this.$refs.mpModal.show();

            },
            complete: function() {
              // complete
            }
          });
        },
        fail: function() {
          consol.log("调用扫码失败");
        }
      });//扫码函数结束
    }
    
  }
};
</script>

<style>
</style>
