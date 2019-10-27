<template>
<div class="page">
    <div class="weui-msg">
        <div class="weui-msg__icon-area"><i class="weui-icon-success weui-icon_msg"></i></div>
        <div class="weui-msg__text-area">
            <h2 class="weui-msg__title">操作成功</h2>
        </div>
        
        <div class="weui-msg__tips-area">
          <p class="weui-msg__tips">感谢你的参与和支持(*￣︶￣)</p>
          <button @click="back">返回首页</button>

        </div>
        <div class="weui-msg__extra-area">
            <div class="weui-footer">
                <p class="weui-footer__text">YNU自强社</p>
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
     
    };
  },
  methods: {
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
