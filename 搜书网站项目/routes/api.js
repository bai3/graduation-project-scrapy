var express = require('express');
var router = express.Router();
var mysql = require('mysql');


var connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '123456',
    database: 'douban',
});
/* GET home page. */
router.get('/search', function(req, res, next) {
    var keyword = req.query.kw;//搜索关键词
    sql = "select * from book_copy2 where name like '%"+keyword+"%' or author like '%"+keyword+"%' or isbn='"+keyword+"'"
    connection.query(sql, function(error, results, fields) {
        if (error) {
            res.send(error)          
        } else {
            if(results.length > 0){
                res.send({ data: results ,code:200,msg:"请求成功"});  
            }else{
                res.send({ data: [] ,code:201,msg:"暂无数据"}); 
            }
        }
    });    
    
});



module.exports = router;
