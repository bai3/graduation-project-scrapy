var app = new Vue({
    el: '#app',
    data:{
        books: [],
        show: 0
    },
    methods:{
        search: function(){
            var _this = this
            var keyword = document.getElementById('search-input').value;
            if(!keyword){
                alert('搜索关键词不能为空,请重新输入')
                return
            }else{
                var url = '/api/search'
                postData = {
                    kw: keyword
                }
                axios.get(url,{params:postData})
                    .then(function(res){
                        if(res.data.code == 200){
                            _this.books = res.data.data; 
                            _this.show = 0                            
                        }else{
                            _this.books = res.data.data; 
                            _this.show = 1
                        }
                        
                    })
                    .catch(function(err){
                        console.log(err)
                    })
            }
        }
    }
})