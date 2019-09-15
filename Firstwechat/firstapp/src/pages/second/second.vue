<template>
<div>
  <div>
<p>回收志愿者会提供专门的二维码扫描二维码既可以记录你的成绩</p>
  </div>
  <div id="action">
     <button @click="touru()">点击扫码投入</button>
  </div>
  <div id="alert">
    <mp-modal ref="mpModal" :title="msg" :content="msg_2+num" :showCancel="false" @confirm="confirm"></mp-modal>
  </div>
</div>

</template>

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
      msg: "投入成功",
      msg_2: "你已经成功投入",
      num: "123"
    };
  },
  methods: {
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
          console.log(res);
          //向链接发送请求
          wx.request({
            url: res.result,
            data: {},
            method: "GET", // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
            // header: {}, // 设置请求的 header
            success: function(res) {
              // success
              console.log("已经向二维码地址发送请求");
              console.log(res.data);
              _this.num = res.data;
              console.log(_this.num);
              _this.$refs.mpModal.show();
            },
            fail: function() {
              // fail
              consol.log("二维码请求失败");
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
