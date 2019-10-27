<template>
<div id="main">
  
  <div v-if="no_code">
    <div class="get_num">
        <h2>请输入投入数量:</h2>
        <input class="yuyue" id="code" type="text" width=50% height="50px" confirm-type="done" v-model="touru_num">
        <mp-modal ref="mpModal" title='请求失败' content="请检查输入" :showCancel="false" @confirm="confirm"></mp-modal>
        <button @click="GetCode">确认</button>
    </div>
  </div>
  <div class="scan_code" v-else>
    <h2>请投入者扫码：{{ touru_num }}</h2>
        <div class="code"><li class="er_code"><img :src="img_url" alt="二维码" class="code"></li></div>
    <button @click="Back">返回</button>

  </div>
</div>   
</template>
<style>
h2{
  font-size: 30px;
  text-align: center
}
input{
  margin: 20px;
  padding: 20px;
  font-size: 30px;
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
      touru_num:'',
      token:'',
      img_url:"data:image/jpg;base64,",
      no_code:true
    };
  },

  mounted() {
   this.onLoad();
  },
  
  methods: {
    onLoad: function (option) {
      let _this = this
     console.log("前："+_this.token);
    _this.token=this.$root.$mp.query.token
    // console.log("后"+_this.token)
    //载入时，重置页面数据
    _this.img_url="data:image/jpg;base64,"
    _this.touru_num="" 
    _this.no_code=true 
    },
    GetCode:function(){
      let _this = this
      console.log("修改后的token:"+_this.token)
      if(_this.touru_num == ''){
        this.$refs.mpModal.show();
      }
      else{
          wx.request({
        url: 'http://127.0.0.1:8000/api/createcode/?token='+_this.token,
        data: {
          token:_this.token,
          num:_this.touru_num
        },
        method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        // header: {}, // 设置请求的 header
        success: function(res){
          console.log(res.data.QR)
          _this.img_url = _this.img_url+res.data.QR
          _this.no_code = false

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
    },

    Back:function(){
      wx.navigateBack({
        delta: 1, // 回退前 delta(默认为1) 页面
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
#code{
  font-size: 20px;
  border: 2px solid #a4c7f2;
}
.yuyue {
  border: 2px solid #0a1016;
  border-radius: 2px;
}
.get_num{
  margin: 5px;
  padding: 5px;
}
.scan_code{
  margin: 5px;
  padding: 5px;
}
.code{
      width: 100%;
      text-align: center
}

</style>
