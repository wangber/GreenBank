<template>
  <div class="container" @click="clickHandle">  
    <div id="index">
      <h1>欢迎了解绿色银行，首页我们为你准备了一个欣赏短短句的好工具哦</h1>
    </div>
    <div id="type">
      <button @click="getOnesen(1)">爱情语句</button>
      <button @click="getOnesen(2)">伤感语句</button>
      <button @click="getOnesen(3)">优美语句</button>
      <button @click="getOnesen(4)">想念的句子</button>
    </div>
    <div id="juzi" class="juzi">
      <p>{{juzi}}</p>
      <p><small>所有句子均来自短文学网https://www.duanwenxue.com/</small> </p>
    </div>
    
  </div>
</template>
<style scoped>
h1{
  background-image: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%);
  margin:20px;
  border: 0px solid;
  border-radius: 5px;

}
button{
  background:#8fd3f4
  }
#type {
  padding: 10px;
  margin: 20px;
}
#type > button {
  margin-top: 20px;
}
#juzi > p > small {
  font-size: 10px;
}
</style>
<script>
import ClickCounter from "@/components/click-counter";

export default {
  data() {
    return {
      msg: "Hello",
      get_data: "onedata",
      juzi: "欣赏一个句子吧！",
      order: 1,
      user_jscode:''
    };
  },
  mounted() {
    console.log("页面已经载入，你的请求有没有执行呢？");
    this.getData();
  },
  methods: {
    
      
    clickHandle() {
      this.msg = "Clicked!!!!!!";
    },
    getData: function() {
      let _this = this;
      wx.request({
        url: "http://127.0.0.1:8000/index/api",
        method: "GET", // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        // header: {}, // 设置请求的 header
        success: function(res) {
          console.log("请求成功，通信" + res.data);
          _this.get_data = res.data;
          // success
        },
        fail: function() {
          console.log("请求失败");
          // fail
        },
        complete: function() {
          // complete
        }
      });
      // this.get_data = "请求之后赋值"
    },
    getOnesen: function(need_order) {
      let _this = this;
      wx.request({
        url: "http://127.0.0.1:8000/index/api/getjuzi",
        data: { type_order: need_order },
        method: "GET", // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        // header: {}, // 设置请求的 header
        success: function(res) {
          _this.juzi = res.data;
          // success
        },
        fail: function() {
          _this.juzi = "句子失踪啦";
          // fail
        },
        complete: function() {
          console.log("一个句子请求已完成");
          // complete
        }
      });
    }
  }
};
</script>

<style scoped>
.message {
  color: red;
  padding: 10px;
  text-align: center;
}
.juzi {
  border: 2px #c0ccfc;
  border-radius: 2px;
  color: black;
  padding: 10px;
  margin: 15px;
  background-image: linear-gradient(-225deg, #69EACB 0%, #EACCF8 48%, #6654F1 100%);
}
</style>
