import decimal
import string
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from  rasa_sdk.executor import  CollectingDispatcher
import mysql.connector
import feedparser
import re

from datetime import datetime


class action_category(Action):

    def name(self) -> Text:
        return "action_category"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            categoryVariable = tracker.get_slot("category")
            # if(categoryVariable=="Lập trình wed" or "lap trinh wed"):
            #     categoryVariable= "Lập trình web"
            categoryArray = []
            index = 0
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="banhang_laravel")
            curCourse = db.cursor()
            codeOfCategory = "SELECT * FROM categories WHERE name LIKE '%{}%'".format(categoryVariable)
            curCourse.execute(codeOfCategory)
            result = curCourse.fetchall()
            for x in result:
                categoryArray.append(x[0])

            db.rollback()
            db.close()

            if (len(categoryArray) > 0):
                codeOfVariable = categoryArray[0]
                courseReturn = []
                slugArray = []
                db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="banhang_laravel")
                curCourse = db.cursor()
                codeOfCategory = "SELECT * FROM product WHERE status='1' and category_id LIKE '%{}%'".format(codeOfVariable)
                curCourse.execute(codeOfCategory)
                result = curCourse.fetchall()
                if (len(result)):
                    for x in result:
                        courseReturn.append(x[1])
                        slugArray.append(x[2])
                    db.rollback()
                    db.close()
                    dispatcher.utter_message("Các sản phẩm " + "'" + categoryVariable + "'" + " hiện có tại website là: ")
                    for x in (courseReturn):
                        i = 1

                        dispatcher.utter_message('%s.' %(index + 1) + x + '.' + 'Xem thông tin sản phẩm tại: http://localhost:8000/danh-muc/%s' %slugArray[index])
                        index += 1
                        i = i + 1

                    return []
                else:
                    dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")


class action_allCategory(Action):

    def name(self) -> Text:
        return "action_allCategory"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            categoryVariable = tracker.get_slot("allcategory")
            categoryArray = []
            slugArray = []
            index = 0
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="banhang_laravel")
            curCourse = db.cursor()
            codeOfCategory = "SELECT * FROM categories where status='1'"
            curCourse.execute(codeOfCategory)
            result = curCourse.fetchall()
            for x in result:
                categoryArray.append(x[1])
                slugArray.append(x[2])
            db.rollback()
            db.close()

            if (len(categoryArray) > 0):
                dispatcher.utter_message("Tất cả các danh mục hiện có tại website là: ")
                for x  in (categoryArray):
                    dispatcher.utter_message('%s.'%(index+1) +x +'.' + 'Xem thông tin sản phẩm tại: http://localhost:8000/danh-muc/%s' %slugArray[index])

                    index+=1
                return []

            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")

class action_priceProduct(Action):

    def name(self) -> Text:
        return "action_priceProduct"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("priceProduct")
            courseArray = []
            slugArray = []

            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="banhang_laravel")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM product WHERE name LIKE '%{}%'".format(courseVariable)
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                courseArray.append(x[9])
                slugArray.append(x[2])
            db.rollback()
            db.close()

            if (len(courseArray) > 0):
                courseReturn = courseArray[0]
                dispatcher.utter_message("Sản phẩm " + courseVariable + " có giá là: " + (courseReturn) + 'VNĐ.' + 'Xem thông tin sản phẩm tại: http://localhost:8000/san-pham/%s' %slugArray[0])

                return []
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này")
        except:
            dispatcher.utter_message("Tôi không hiểu!")



class action_quantity(Action):

    def name(self) -> Text:
        return "action_quantity"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("quantity")
            courseArray = []
            slugArray = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="banhang_laravel")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM product WHERE name LIKE '%{}%'".format(courseVariable)
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                courseArray.append(x[3])
                slugArray.append(x[2])
            db.rollback()
            db.close()

            if (len(courseArray) > 0):
                courseReturn = courseArray[0]
                if(courseReturn!=0):
                    dispatcher.utter_message("Sản phẩm " + courseVariable + " vẫn còn hàng. " + 'Xem thông tin sản phẩm tại: http://localhost:8000/san-pham/%s' %slugArray[0])
                else:
                    dispatcher.utter_message("Sản phẩm " + courseVariable + " đã hết hàng. " + 'Xem thông tin sản phẩm tại: http://localhost:8000/san-pham/%s' %slugArray[0])


                return []
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này")
        except:
            dispatcher.utter_message("Tôi không hiểu!")

class action_multiDiscount(Action):

    def name(self) -> Text:
        return "action_multiDiscount"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("priceProduct")
            courseArray = []
            slugArray = []
            index = 0
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="banhang_laravel")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM product WHERE discount > 0"
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                courseArray.append(x[1])
                slugArray.append(x[2])
            db.rollback()
            db.close()

            if (len(courseArray) > 0):
                dispatcher.utter_message("Tất cả các sản phẩm hiện đang giảm giá tại website là: ")

                for x in (courseArray):
                    dispatcher.utter_message('%s.' % (index + 1) + x + '.' + 'Xem thông tin sản phẩm tại: http://localhost:8000/san-pham/%s' %slugArray[index])
                    index += 1

                return []
            else:
                dispatcher.utter_message("Không có sản phẩm nào hiện đang giảm giá!")
        except:
            dispatcher.utter_message("Tôi không hiểu!")


class action_discount(Action):

    def name(self) -> Text:
        return "action_discount"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            courseVariable = tracker.get_slot("discountSingle")
            courseArray = []
            slugArray = []
            db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="", database="banhang_laravel")
            curCourse = db.cursor()
            codeOfCourse = "SELECT * FROM product WHERE discount >0".format(courseVariable)
            curCourse.execute(codeOfCourse)
            result = curCourse.fetchall()
            for x in result:
                courseArray.append(x[11])
                slugArray.append(x[2])
            db.rollback()
            db.close()

            if (len(courseArray) > 0):
                courseReturn = courseArray[0]
                if(courseReturn!=0):
                    dispatcher.utter_message("Sản phẩm " + courseVariable + " hiện tại đang giảm giá. " + 'Xem thông tin sản phẩm tại: http://localhost:8000/san-pham/%s' %slugArray[0])
                else:
                    dispatcher.utter_message("Sản phẩm " + courseVariable + " không có giảm giá. " + 'Xem thông tin sản phẩm tại: http://localhost:8000/san-pham/%s' %slugArray[0])
                return []
            else:
                dispatcher.utter_message("0 kết quả cho tìm kiếm này")
        except:
            dispatcher.utter_message("Tôi không hiểu!")
