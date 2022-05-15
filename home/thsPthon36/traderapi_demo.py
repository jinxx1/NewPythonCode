#encoding:utf-8
from hxtrade import HxTraderApi
from hxtrade import HX_LOG_LEVEL
from hxtrade import HX_EXCHANGE_TYPE
from hxtrade import HX_PRICE_TYPE
from hxtrade import HX_ACTION_TYPE
from hxtrade import HX_BUSINESS_TYPE
from hxtrade import HX_CURRENCY_TYPE
from hxtrade import HX_ORDER_STATUS_TYPE

import configparser
import logging
import sys
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s') 

class TradeSpi:
    '''交易推送'''

    def SetTrade(self,trade):
        self._trade=trade

   
    #报单通知
    def OnOrderChange(self,order_info,  error, session_id):
        '''
        :param order_info:dict
        :param error:dict
        :param session_id:int
        '''
        #logging.debug('order_info=%s,error=%s,session_id=%d',order_info,error,session_id)
        
        def cancelOrder(order_no):
            logging.debug('OnOrderChange,CancelOrder Begin,order_no=%d,session_id=%d',order_no,session_id)
            cancel_no=trade.CancelOrder(order_no=order_no,session_id=session_id)
            if cancel_no == 0:
                logging.error('OnOrderChange,CancelOrder Failed:%s from session_id(%d)',trade.GetApiLastError(),session_id)
            else:
                logging.debug('OnOrderChange,CancelOrder Success,cancel_no=%d',cancel_no)
        
        switcher={
           HX_ORDER_STATUS_TYPE.HX_ORDER_STATUS_TYPE_INIT              :lambda order_no : logging.debug('order_no=%d,未报',order_no),
           HX_ORDER_STATUS_TYPE.HX_ORDER_STATUS_TYPE_IN_PROCESS        :lambda order_no: logging.debug('order_no=%d,正报',order_no),
           HX_ORDER_STATUS_TYPE.HX_ORDER_STATUS_TYPE_READY             :cancelOrder, #lambda order_no: logging.debug('order_no=%d,已报',order_no),
           HX_ORDER_STATUS_TYPE.HX_ORDER_STATUS_TYPE_INVALID           :lambda order_no: logging.debug('order_no=%d,废单',order_no),
           HX_ORDER_STATUS_TYPE.HX_ORDER_STATUS_TYPE_PART_TRADED       :lambda order_no: logging.debug('order_no=%d,部分成交',order_no),
           HX_ORDER_STATUS_TYPE.HX_ORDER_STATUS_TYPE_ALL_TRADED        :lambda order_no: logging.debug('order_no=%d,全部成交',order_no),
           HX_ORDER_STATUS_TYPE.HX_ORDER_STATUS_TYPE_PART_CANCELED     :lambda order_no: logging.debug('order_no=%d,部分撤单',order_no),
           HX_ORDER_STATUS_TYPE.HX_ORDER_STATUS_TYPE_ALL_CANCELED      :lambda order_no: logging.debug('order_no=%d,全部撤单',order_no),
           HX_ORDER_STATUS_TYPE.HX_ORDER_STATUS_TYPE_INTERNAL_CANCELED :lambda order_no: logging.debug('order_no=%d,内部撤单',order_no),
           HX_ORDER_STATUS_TYPE.HX_ORDER_STATUS_TYPE_UNKNOWN           :lambda order_no: logging.error('order_no=%d,未知状态',order_no),
        }
      
        switcher[order_info['order_status']](order_info['order_no_source']) 
        
        pass
        

    #成交通知
    def OnTradeChange(self,trade_info, session_id):
        '''
        :param trade_info:dict
        :param session_id:int
        '''
        logging.debug('trade_info=%s,session_id=%d',trade_info,session_id)

    #撤单出错响应
    def OnCancelOrderError(self,cancel_info, error, session_id):
        '''
        :param cancel_info:dict
        :param error:dict
        :param session_id:int
        '''
        logging.debug('cancel_info=%s,error=%s,session_id=%d',cancel_info,error,session_id)

    #请求查询报单响应
    def OnQueryOrderRsp(self,order_info, error, request_id, is_last, session_id):
        '''
        :param order_info:dict
        :param error:dict
        :param request_id:int
        :param is_last:bool
        :param session_id:int
        '''
        

        #logging.debug('orade_info=%s,error=%s,request_id=%d,is_last=%s,session_id=%d',order_info,error,request_id,is_last,session_id)
        pass


    #请求查询成交响应
    def OnQueryTradeRsp(self,trade_info, error, request_id, is_last, session_id):
        '''
        :param trade_info:dict
        :param error:dict
        :param requst_id:int
        :param is_last:bool
        :param session_id:int
        '''

        #logging.debug('trade_info=%s',trade_info)
        pass

    #请求查询投资者持仓响应
    def OnQueryPositionRsp(self,position, error, request_id, is_last, session_id):
        '''
        :param position:dict
        :param error:dict
        :param request_id:int
        :param is_last:bool
        :param session_id:int
        '''
        #logging.debug('position=%s',position)
        pass

    #请求查询资金账户
    def OnQueryAssetRsp(self,asset, error, request_id, is_last, session_id):
        '''
        :param asset:dict
        :param error:dict
        :param request_id:int
        :param is_last:bool
        :param session_id:int
        '''
        #logging.debug('asset=%s',asset)
        pass

if __name__ == '__main__':

    #解析ini配置
    conf=configparser.ConfigParser()
    conf.read('simple_py_demo.ini',encoding='utf-8')

    #创建交易api
 
    trade=HxTraderApi(terminal_id=conf.getint('client_info','terminal_id'),save_file_path=conf.get('client_info','save_file_path'),log_level=HX_LOG_LEVEL.HX_LOG_LEVEL_NOLOG)

    #设置license
    trade.SetDeveloperKey(key=conf.get('client_info','license'))

    #注册spi
    spi=TradeSpi()
    #设置trade用于在spi回调函数中作相关操作
    spi.SetTrade(trade)

    trade.RegisterSpi(

                      OnOrderChange=spi.OnOrderChange,
                      OnTradeChange=spi.OnTradeChange,
                      OnCancelOrderError=spi.OnCancelOrderError,
                      OnQueryOrderRsp=spi.OnQueryOrderRsp,
                      OnQueryTradeRsp=spi.OnQueryTradeRsp,
                      OnQueryPositionRsp=spi.OnQueryPositionRsp,
                      OnQueryAssetRsp=spi.OnQueryAssetRsp 
                     )
    
    #登录
    
    session_id=trade.Login(ip=conf.get('client_info','trade_ip'),
                           port=conf.getint('client_info','trade_port'),
                           user=conf.get('client_info','user'),
                           password=conf.get('client_info','password')
                           )

    if session_id == 0 :
        logging.error('Login Failed:%s',trade.GetApiLastError())
        sys.exit()
    else:
        logging.debug('Login Success,session_id=%d',session_id)

    #下单
    order_info={
       'symbol':'600519',                             #市场代码
       'exchange':HX_EXCHANGE_TYPE.HX_EXCHANGE_SH,    #市场
       'price':1,                                  #价格
       'quantity':100,                                #数量
       'price_type':HX_PRICE_TYPE.HX_PRICE_LIMIT,     #价格类型
       'action':HX_ACTION_TYPE.HX_ACTION_TYPE_BUY,    #委托类型 
       'business_type':HX_BUSINESS_TYPE.HX_BUSINESS_TYPE_STOCK #业务类型 
       }

    order_no=trade.InsertOrder(order_info,session_id)

    if order_no == 0 :
        logging.error('InsertOrder Failed:%s from session_id(%d)',trade.GetApiLastError(),session_id)
    else:
        logging.debug("InsertOrder Success,order_no=%d",order_no)
    

    #指定委托号查询    
    code=trade.ReqOrders(query_param={'order_no':order_no},session_id=session_id,request_id=110)
    if code < 0 :
        logging.error('ReqOrders Failed:%s',trade.GetApiLastError())
    else:
        logging.debug('ReqOrders by order_no Success')
    
    #查询所有委托
    code=trade.ReqOrders(query_param={},session_id=session_id,request_id=110)
    if code < 0 :
        logging.error('ReqOrders Failed:%s',trade.GetApiLastError())
    else:
        logging.debug('ReqOrders all Success')
    

    #根据委托号查询成交    
    code=trade.ReqTradesByHxID(order_no=order_no,session_id=session_id,request_id=110)
    if code <0 :
        logging.error('ReqTradesByHxID Failed:%s',trade.GetApiLastError())
    else:
        logging.debug('ReqTradesByHxID Success')

    code=trade.ReqTrades(query_param={'symbol':'60030'},session_id=session_id,request_id=110)
    if code < 0 :
        logging.error('ReqTrades Failed:%s',trade.GetApiLastError())
    else:
        logging.debug('ReqTrades Success')
    

    #查询资产
    code=trade.ReqAsset(session_id=session_id,request_id=110)
    if code<0 :
        logging.error('ReqAsset Failed:%s',trade.GetApiLastError())
    else:
        logging.debug("ReqAsset Success")
   
    #回车退出程序
    input('Press <enter> exit\n')
    trade.Logout(session_id)

