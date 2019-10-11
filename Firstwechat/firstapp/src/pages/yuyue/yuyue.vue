<template>
<div id="main">
  <p>请输入宿舍号：</p>
    <input type="text" id="yuyue" class="yuyue" width=50% height="50px" confirm-type="done" v-model="yuyue_location">
    <mp-modal ref="mpModal" :title="su" :content="su_msg" :showCancel="false" @confirm="confirm"></mp-modal>
    <mp-button type="primary" size="normal" btnClass="mb15" @click="back()">返回首页</mp-button>
    <mp-button type="primary" size="normal" btnClass="mb15" @click="sendlocation()">提交预约</mp-button>
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
      yuyue_location: "请输入你的宿舍号",
      su:"抱歉，预约失败",
      su_msg:"请检查你的输入，之后再次预约，谢谢你(*^▽^*)",
    };
  },
  methods: {
    sendlocation: function() {
      console.log("用来作判断的输入内容："+this.yuyue_location)
      if (this.yuyue_location ==''|this.yuyue_location=='请输入你的宿舍号'){
              this.su="抱歉，预约失败"
              this.su_msg="请检查你的输入，之后再次预约，谢谢你的支持！"
              console.log("本该失败"+this.su)
              this.$refs.mpModal.show();
      }
      else{
        this.su="预约成功"
        this.su_msg="我们将会在回收当晚到达你的宿舍，为避免打扰，有不方便的情况请提前和我们联系哦(*^▽^*)"
        let _this = this
        wx.request({
          url: 'http://127.0.0.1:8000/api/yuyue/',
          method: 'POST', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
          data:{
            location:_this.yuyue_location
          },
          header:{
            'content-type': 'application/x-www-form-urlencoded',
          }, // 设置请求的 header
          success: function(res){
            console.log("预约地址填写："+res.data)
          },
          fail: function() {
            _this.su="预约失败"
            _this.su_msg="请检查你的输入，之后再次预约，谢谢你的支持！"
          },
          complete: function() {
            // complete
          }
        })
        this.$refs.mpModal.show();
      }
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
.yuyue {
  border: 2px solid #0a1016;
  border-radius: 2px;
}
</style>
