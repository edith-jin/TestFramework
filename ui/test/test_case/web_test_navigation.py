# coding=utf-8

import unittest
import time
from common.lib.base_yaml import Yaml
from ui.view.businessview.web.common.login_business import simple_login
from ui.lib.base_runner import BaseWebTestCase
from ui.lib.browser_engine import Logger, web_config_path
from ui.view.businessview.web.admin.navigation_business import *

class Admin_navigation(BaseWebTestCase):
    def __init__(self, *args, **kwargs):
        BaseWebTestCase.__init__(self, *args, **kwargs)

    @classmethod
    def setUpClass(cls):
        super(Admin_navigation, cls).setUpClass()
        cls.driver = simple_login()
        cls.data = Yaml(web_config_path).read()
        cls.env = cls.data['env']
        url = cls.data['portal'][cls.env] + '/admin'
        cls.driver.get(url)

    def test_admin_navigation(self):
        navigation_business = Navigation_business(self.driver)

        for name, item in navigation_business.menu.items():
            with self.subTest(name):
                if item.is_clickable:
                    if item.has_subitems:
                        continue
                    item.click()
                    self.validate_tab_page(navigation_business.menu, name)
                continue

    def validate_tab_page(self, dict_menu, item_name):
        item:Navigation_business.Admin_settings_menu_item = dict_menu[item_name]
        if item.tab_by is None:
            return
        if item.parent is not None:
            #确保当前父节点已展开
            parent = dict_menu[item.parent]
            is_parent_expanded = parent.expand()
            #点击并确认右侧内容
            if is_parent_expanded:
                item.click()
                ele_tab_page = item.obj.find_element(*item.tab_by)
                self.assertIsNotNone(ele_tab_page, ('页面'+ item.name + '没有显示'))
                #父节点下唯一子元素
                self.assertEqual(item.tab_page_number(),1,"不是唯一子元素")
                

class Admin_navigation_dropdowmlist(Admin_navigation):
    def test_admin_navigation(self):
        navigation_business = Navigation_business(self.driver)

        for name, item in navigation_business.menu.items():
            with self.subTest(name):
                if item.is_clickable:
                    if item.has_subitems:
                        time.sleep(2)
                        self.assertTrue(item.contract(), name+"没有收起子项目的功能")
                        self.assertTrue(item.expand(), name+"没有展开子项目的功能")
                        continue
                    if item.parent is None:
                        self.assertTrue(item.is_present(),'确认Admin settings标签不存在')
                        continue
                continue

if __name__ == '__main__':
    unittest.main()