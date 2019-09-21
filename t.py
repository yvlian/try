import os
import time
import sys
import logging
import networkx as nx
from androguard.core.bytecodes.apk import APK #创建APK文件对象的类,用于访问APK文件中的所有元素
from androguard.core.bytecodes.dvm import DalvikVMFormat#DEX文件对象的类,解析APK文件中的classes.dex
from androguard.core.analysis.analysis import Analysis#分析结果对象的类,分析DEX文件对象

def get_androguard_info():
    #APK、DalvikVMFormat、VMAnalysis类参数属性、方法
    androguard_info = dict()
    androguard_info['APK_info'] = dir(APK)
    androguard_info['DalvikVMFormat_info'] = dir(DalvikVMFormat)
    androguard_info['VMAnalysis_info'] = dir(Analysis)
    return androguard_info

def get_apk_info(apkfile):
    apk_info = {}
    apk_object = APK(apkfile)
    #print apk_object.xml["AndroidManifest.xml"].toxml()
    apk_info['manifest_xml'] = apk_object.get_android_manifest_xml() #获取manifest文件
    apk_info['dex_file'] = DalvikVMFormat(apk_object.get_dex()) #获取dex文件
    apk_info['app_name'] = apk_object.get_app_name() #获取APK应用
    apk_info['apkfile_name'] = apk_object.get_filename() #获取APK文件名
    apk_info['signature'] = apk_object.get_signature() #获取APK签名
    apk_info['android_version'] = apk_object.get_androidversion_code() #获取Android版本名
    apk_info['is_valid'] = apk_object.is_valid_APK() #判断APK是否有效
    apk_info['package'] = apk_object.get_package() #获取package名
    apk_info['activities'] = apk_object.get_activities() #获取APK所有activity名称列表
    apk_info['main_activity'] = apk_object.get_main_activity() #获取APK主activity名称
    apk_info['services'] = apk_object.get_services() #获取APK所有service名称列表
    apk_info['receivers'] = apk_object.get_receivers() #获取APK所有receiver名称列表
    apk_info['providers'] = apk_object.get_providers() #获取APK所有provider名称列表
    apk_info['files'] = apk_object.get_files() #获取APK文件列表
    apk_info['show'] = apk_object.show() #APK基本信息
    # 获取APK权限相关信息
    apk_info['permissions'] = apk_object.get_permissions()
    apk_info['declared_permissions'] = apk_object.get_declared_permissions()
    apk_info['certificate'] = apk_object.get_certificate()
    Analysis(apk_info['dex_file']).get_call_graph()
    return apk_info

if __name__ == '__main__':
    logger = logging.getLogger()#创建logger对象，
    logger.setLevel(logging.DEBUG) # logger的总开关，只有大于Debug的日志才能被logger对象处理,DEBUG < INFO < WARNING < ERROR < CRITICAL
    format = logging.Formatter(fmt="%(asctime)s - %(levelname)s: %(message)s",datefmt='%Y-%m-%d %H:%M:%S')    # output format
    sh = logging.StreamHandler(stream=sys.stdout)    # output to standard output
    sh.setFormatter(format)
    logger.addHandler(sh)
    logger.info("This is androguard class methods and properties.")
    # print (get_androguard_info())
    logger.info("This is APK info.")
    print(get_apk_info('1.apk'))

