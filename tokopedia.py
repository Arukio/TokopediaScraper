# /*************************************************************************
# * 
# * Tokopedia Scrape for Tokopedia [Dropship]
# * __________________
# * 
# *  [2018] Created By Oky Mikhael 
# *  All Rights Reserved.
# * 
# * Message:    Terimakasih sudah menggunakan program ini
# *             walau memang kurang dari sempurna tetapi untuk
# *             keperluan dropship aplikasi ini sudah mendukung
# *             walau memang saya sadari bukan untuk orang yang 
# *             tidak paham tentang lingkup ini (Coding).
# *              
# *             Maaf jika saya memang membuat program ini tanpa UI
# *             karena saya bisa dibilang sangat baru untuk bahasa
# *             program yang satu ini yaitu Python
# *              
# *             Yup itu juga alasan mengapa saya menggunakan Python 
# *             versi 2.7 sebagai requipment dikarenakan saya tidak 
# *             tahu apa-apa dulunya (sudah Terlanjur)
# *              
# * Requipment Untuk Menggunakan Program Ini :
# *             - Sistem Operasi : Windows, Linux, OS X
# *             - Python 2.7                     
# *             - Library untuk python : lxml, fake_useragent, requests                      
# *               (Mungkin ada yang terlewatkan)
# * 
# * Untuk lebih jelasnya cara penggunaan dilihat di youtube channel saya : 
# *             - Buka link youtube dibawah 
# *             - cari video dengan kata kunci "Cara menggunakan Aplikasi Tokopedia Scrape for Tokopedia Dropship"
# *             - Kemungkinan ada beberapa part untuk penjelasan (Comment Jika Masih Belum Paham)
# * 
# * Contact Me If Have Problem With Instalation or etc :
# * Instagram : https://www.instagram.com/kymkhl24/
# * 
# * My Bussiness Account
# * WA : +62 831-2918-5005
# * Gitlab : https://gitlab.com/okymikhael
# * Youtube Channel : https://www.youtube.com/channel/UCS0g6trSzfPUT5c9IxEMFFg
# * 
# *************************************************************************/

from config import *
import urllib
from lxml import html
import lxml.html as LH
from lxml import etree
import requests
from fake_useragent import UserAgent

import csv
from datetime import datetime

import os

import urllib2, cookielib
import numpy as np
from string import maketrans
import re
from pprint import pprint

import json

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def ambil(dataSementara, jumlah):

    # link tokopedia untuk diambil (rubah shop_id sesuai shop_id yang diinginkan)
    link = 'https://ace.tokopedia.com/search/v2.6/product?shop_id={}&rows=1000000&start={}'.format(shop_id,jumlah)

    page = urllib2.Request(link, headers=hdr)

    try:
        task = urllib2.urlopen(page)
    except urllib2.HTTPError, e:
        print e.fp.read()

    content = task.read()
    data = json.loads(content) 
    print link 
    pemilik_barang = data['data'][0]['shop']['name']

    sum = 0

    # filename = 'test.json'

    # myarray = {}

    format = []

    while (sum < len(data['data'])):
        final = data['data'][sum]["uri"]
        format.append(final)
        sum = sum + 1

    initiator = 0

    while (initiator < len(format)) :
        # Scrap one page
        ua = UserAgent()
        headers = {'User-Agent': ua.random}

        try:
            response = requests.get(format[initiator], headers=headers)
        except requests.exceptions.Timeout:
            print 'Request Time Out'
        except requests.exceptions.TooManyRedirects:
            print 'Bad URL'
        except requests.exceptions.RequestException as e:
            print e

        # response = requests.get(format[initiator], headers=headers)
        sourceCode = response.content
        parser_page = html.fromstring(sourceCode) 

        get_nama = parser_page.xpath('//h1[@class="rvm-product-title"]//text()')
        nama = get_nama[1]
        description = parser_page.xpath('//div[@itemprop="description"]//node()')
        get_harga = parser_page.xpath('//span[@itemprop="price"]//text()')
        harga = get_harga[0].replace('.', '').replace('\n', '')
        beratOps = parser_page.xpath('//div[@class="rvm-shipping-content"]//text()')
        berat = beratOps[0].replace(' ', '').replace('\n', '').replace('gr', '').replace('.', '')
        minbeli = parser_page.xpath('//div[@class="rvm-product-info--item_value mt-5"]//text()')
        minBeli = minbeli[1].replace(' ', '').replace('\n', '')
        get_kondisi = parser_page.xpath('//div[@class="rvm-product-info--item_value mt-5"]//text()')
        kondisi = get_kondisi[0].replace(' ', '').replace('\n', '')
        kategori = parser_page.xpath('//ul[@class="breadcrumb"]//text()')
        # kategori_a = kategori[5][:-1]
        # kategori_b = kategori[10][:-1]
        image = parser_page.xpath('//div[@class="content-img-relative"]//img//@src')

        try:
            kategori_a = kategori[5][:-1]
        except IndexError:
            kategori_a = 0

        try:
            kategori_b = kategori[10][:-1]
        except IndexError:
            kategori_b = 0

        try:
            kategori_c = kategori[15][:-1]
        except IndexError:
            kategori_c = 0

        if kategori_c > 1 or kategori_b > 1 or kategori_a > 1 and int(berat) > 10 :

            if kategori_c == 'Polo Shirt' : real_kategori = 1774
            elif kategori_c == 'Kaos' : real_kategori = 1769
            elif kategori_c == 'Kemeja' : real_kategori = 1770
            elif kategori_c == 'Blouse' : real_kategori = 1771
            elif kategori_c == 'Tank Top' : real_kategori = 1772
            elif kategori_c == 'Crop Top' : real_kategori = 1773
            elif kategori_c == 'Legging' : real_kategori = 1781
            elif kategori_c == 'Celana Crop' : real_kategori = 1779
            elif kategori_c == 'Hot Pants' : real_kategori = 1776
            elif kategori_c == 'Celana Jeans' : real_kategori = 1778
            elif kategori_c == 'Celana Panjang' : real_kategori = 1780
            elif kategori_c == 'Celana Pendek' : real_kategori = 1777
            elif kategori_c == 'Rok Midi' : real_kategori = 1785
            elif kategori_c == 'Rok Maxi' : real_kategori = 1786
            elif kategori_c == 'Rok Mini' : real_kategori = 1783
            elif kategori_c == 'Midi Dress' : real_kategori = 1764
            elif kategori_c == 'Maxi Dress' : real_kategori = 1765
            elif kategori_c == 'Jumpsuit' : real_kategori = 1766
            elif kategori_c == 'Mini Dress' : real_kategori = 1763
            elif kategori_c == 'Blazer' : real_kategori = 1813
            elif kategori_c == 'Cardigan' : real_kategori = 1797
            elif kategori_c == 'Hoodie' : real_kategori = 1812
            elif kategori_c == 'Vest' : real_kategori = 1815
            elif kategori_c == 'Sweater' : real_kategori = 1810
            elif kategori_c == 'Coat' : real_kategori = 1811
            elif kategori_c == 'Jaket' : real_kategori = 1814
            elif kategori_b == 'Setelan' : real_kategori = 1767
            elif kategori_c == 'Dress Batik' : real_kategori = 1792
            elif kategori_c == 'Kain Batik' : real_kategori = 1793
            elif kategori_c == 'Bawahan Batik' : real_kategori = 1791
            elif kategori_c == 'Batik Couple' : real_kategori = 1794
            elif kategori_c == 'Kebaya' : real_kategori = 1967
            elif kategori_c == 'Blouse Batik' : real_kategori = 1790
            elif kategori_c == 'Celana Dalam' : real_kategori = 1823
            elif kategori_c == 'G-String' : real_kategori = 1825
            elif kategori_c == 'Korset' : real_kategori = 1824
            elif kategori_c == 'Lingerie' : real_kategori = 1821
            elif kategori_c == 'BRA' : real_kategori = 1822
            elif kategori_c == 'Clutch' : real_kategori = 1918
            elif kategori_c == 'Hand Bag' : real_kategori = 1919
            elif kategori_c == 'Shoulder Bag' : real_kategori = 1920
            elif kategori_c == 'Tas Selempang' : real_kategori = 1921
            elif kategori_c == 'Tote Bag' : real_kategori = 1922
            elif kategori_c == 'Aksesoris Tas' : real_kategori = 1923
            elif kategori_c == 'Tas Kosmetik' : real_kategori = 1969
            elif kategori_c == 'Backpack' : real_kategori = 1917
            elif kategori_c == 'Sneakers' : real_kategori = 1908
            elif kategori_c == 'Sandal' : real_kategori = 1907
            elif kategori_c == 'Sepatu Sandal' : real_kategori = 1906
            elif kategori_c == 'Loafers' : real_kategori = 1910
            elif kategori_c == 'Boots' : real_kategori = 1911
            elif kategori_c == 'Kaos Kaki' : real_kategori = 1912
            elif kategori_c == 'Flat Shoes' : real_kategori = 1913
            elif kategori_c == 'Wedges' : real_kategori = 1914
            elif kategori_c == 'Heels' : real_kategori = 1915
            elif kategori_c == 'Slip On' : real_kategori = 1909
            elif kategori_c == 'Jam Tangan LED' : real_kategori = 1977
            elif kategori_c == 'Jam Tangan Digital' : real_kategori = 1948
            elif kategori_c == 'Jam Tangan Analog' : real_kategori = 1949
            elif kategori_c == 'Anting' : real_kategori = 1928
            elif kategori_c == 'Logam Mulia' : real_kategori = 2098
            elif kategori_c == 'Kalung' : real_kategori = 1925
            elif kategori_c == 'Gelang' : real_kategori = 1926
            elif kategori_c == 'Cincin' : real_kategori = 1927
            elif kategori_c == 'Liontin' : real_kategori = 1931
            elif kategori_c == 'Bros' : real_kategori = 1930
            elif kategori_c == 'Kacamata Hitam' : real_kategori = 1934
            elif kategori_c == 'Frame Kacamata' : real_kategori = 1935
            elif kategori_c == 'Dompet Wanita' : real_kategori = 1936
            elif kategori_c == 'Ikat Pinggang Wanita' : real_kategori = 1937
            elif kategori_c == 'Scarf & Shawl' : real_kategori = 1938
            elif kategori_c == 'Kacamata' : real_kategori = 1952
            elif kategori_c == 'Sarung Tangan Fashion' : real_kategori = 1971
            elif kategori_c == 'Topi Wanita' : real_kategori = 1933
            elif kategori_c == 'Rambut Palsu' : real_kategori = 1945
            elif kategori_c == 'Hair Extension' : real_kategori = 1943
            elif kategori_c == 'Mahkota & Headpiece' : real_kategori = 1944
            elif kategori_c == 'Jepitan Rambut' : real_kategori = 1940
            elif kategori_c == 'Bando' : real_kategori = 1941
            elif kategori_c == 'Ikat Rambut' : real_kategori = 1942
            elif kategori_c == 'Jam Tangan Couple' : real_kategori = 1964
            elif kategori_c == 'Aksesoris Couple' : real_kategori = 1965
            elif kategori_c == 'Baju Couple' : real_kategori = 1966
            elif kategori_c == 'Cincin Couple' : real_kategori = 1963
            elif kategori_c == 'Piyama' : real_kategori = 1817
            elif kategori_c == 'Celana Tidur' : real_kategori = 1818
            elif kategori_c == 'Daster' : real_kategori = 1819
            elif kategori_c == 'Jarum Jahit' : real_kategori = 2074
            elif kategori_c == 'Manekin' : real_kategori = 2083
            elif kategori_c == 'Resleting' : real_kategori = 2078
            elif kategori_c == 'Patch' : real_kategori = 2084
            elif kategori_c == 'Alat Ukur Baju' : real_kategori = 2080
            elif kategori_c == 'Benang' : real_kategori = 2076
            elif kategori_c == 'Kancing' : real_kategori = 2075
            elif kategori_c == 'Payet' : real_kategori = 2081
            elif kategori_c == 'Peniti' : real_kategori = 2077
            elif kategori_c == 'Mesin Jahit' : real_kategori = 2079
            elif kategori_c == 'Kemeja Casual' : real_kategori = 1806
            elif kategori_c == 'Kaos Tanpa Lengan' : real_kategori = 1807
            elif kategori_c == 'Kaos' : real_kategori = 1808
            elif kategori_c == 'Polo Shirt' : real_kategori = 1809
            elif kategori_c == 'Kemeja Formal' : real_kategori = 1805
            elif kategori_c == 'Sneakers' : real_kategori = 1845
            elif kategori_c == 'Loafers' : real_kategori = 1847
            elif kategori_c == 'Boots' : real_kategori = 1848
            elif kategori_c == 'Pantofel' : real_kategori = 1850
            elif kategori_c == 'Sepatu Sandal' : real_kategori = 1844
            elif kategori_c == 'Slip On' : real_kategori = 1846
            elif kategori_c == 'Kaos Kaki' : real_kategori = 1849
            elif kategori_c == 'Perawatan Sepatu' : real_kategori = 1851
            elif kategori_c == 'Sandal' : real_kategori = 1843
            elif kategori_c == 'Celana Pendek' : real_kategori = 1827
            elif kategori_c == 'Celana Jeans' : real_kategori = 1828
            elif kategori_c == 'Celana Panjang' : real_kategori = 1826
            elif kategori_c == 'Cardigan' : real_kategori = 1831
            elif kategori_c == 'Jas' : real_kategori = 1835
            elif kategori_c == 'Jaket' : real_kategori = 1836
            elif kategori_c == 'Sweater' : real_kategori = 1832
            elif kategori_c == 'Vest' : real_kategori = 1837
            elif kategori_c == 'Hoodie' : real_kategori = 1834
            elif kategori_c == 'Coat' : real_kategori = 1833
            elif kategori_c == 'Strap Jam Tangan' : real_kategori = 1874
            elif kategori_c == 'Jam Tangan Analog' : real_kategori = 1873
            elif kategori_c == 'Jam Tangan LED' : real_kategori = 1875
            elif kategori_c == 'Jam Tangan Digital' : real_kategori = 1872
            elif kategori_c == 'Backpack' : real_kategori = 1852
            elif kategori_c == 'Tas Travel' : real_kategori = 1853
            elif kategori_c == 'Briefcase' : real_kategori = 1854
            elif kategori_c == 'Tas Selempang' : real_kategori = 1855
            elif kategori_c == 'Clutch' : real_kategori = 1968
            elif kategori_c == 'Waist Bag' : real_kategori = 1959
            elif kategori_c == 'Celana Batik' : real_kategori = 1830
            elif kategori_c == 'Kemeja Batik' : real_kategori = 1829
            elif kategori_c == 'Kacamata Hitam' : real_kategori = 1864
            elif kategori_c == 'Kacamata' : real_kategori = 1865
            elif kategori_c == 'Dompet Pria' : real_kategori = 1867
            elif kategori_c == 'Ikat Pinggang Pria' : real_kategori = 1868
            elif kategori_c == 'Dasi' : real_kategori = 1870
            elif kategori_c == 'Sarung Tangan Fashion' : real_kategori = 1970
            elif kategori_c == 'Topi Pria' : real_kategori = 1863
            elif kategori_c == 'Celana Dalam' : real_kategori = 1841
            elif kategori_c == 'Boxer' : real_kategori = 1842
            elif kategori_c == 'Kaos Dalam' : real_kategori = 1840
            elif kategori_c == 'Cincin' : real_kategori = 1859
            elif kategori_c == 'Gelang' : real_kategori = 1858
            elif kategori_c == 'Batu Mulia & Batu Alam' : real_kategori = 1862
            elif kategori_c == 'Anting' : real_kategori = 1860
            elif kategori_c == 'Kalung' : real_kategori = 1857
            elif kategori_c == 'Piyama' : real_kategori = 1838
            elif kategori_c == 'Celana Tidur' : real_kategori = 1839
            elif kategori_c == 'Kemeja Muslim' : real_kategori = 1884
            elif kategori_c == 'Blouse Muslim' : real_kategori = 1881
            elif kategori_c == 'Baju Koko' : real_kategori = 1883
            elif kategori_c == 'Manset Muslim' : real_kategori = 1882
            elif kategori_c == 'Rok Muslim' : real_kategori = 1886
            elif kategori_c == 'Palazzo' : real_kategori = 1888
            elif kategori_c == 'Legging' : real_kategori = 1887
            elif kategori_c == 'Celana Muslim' : real_kategori = 1885
            elif kategori_c == 'Jumpsuit' : real_kategori = 1890
            elif kategori_c == 'Kaftan' : real_kategori = 1958
            elif kategori_c == 'Gamis' : real_kategori = 1889
            elif kategori_c == 'Abaya' : real_kategori = 1891
            elif kategori_c == 'Cape' : real_kategori = 1955
            elif kategori_c == 'Coat' : real_kategori = 1957
            elif kategori_c == 'Vest' : real_kategori = 1956
            elif kategori_c == 'Cardigan' : real_kategori = 1954
            elif kategori_c == 'Khimar' : real_kategori = 1902
            elif kategori_c == 'Pashmina' : real_kategori = 1903
            elif kategori_c == 'Hijab Segi Empat' : real_kategori = 1904
            elif kategori_c == 'Ciput' : real_kategori = 1900
            elif kategori_c == 'Hijab Instan' : real_kategori = 1901
            elif kategori_c == 'Brooch' : real_kategori = 1898
            elif kategori_c == 'Headpiece' : real_kategori = 1897
            elif kategori_c == 'Tasbih' : real_kategori = 1896
            elif kategori_c == 'Sajadah' : real_kategori = 1895
            elif kategori_c == 'Mukena' : real_kategori = 1892
            elif kategori_c == 'Peci' : real_kategori = 1894
            elif kategori_c == 'Sarung' : real_kategori = 1893
            elif kategori_b == 'Baju Muslim Anak' : real_kategori = 1961
            elif kategori_b == 'Setelan Muslim' : real_kategori = 1960
            elif kategori_c == 'Bando' : real_kategori = 2065
            elif kategori_c == 'Ikat Rambut' : real_kategori = 2067
            elif kategori_c == 'Jepitan Rambut' : real_kategori = 2066
            elif kategori_c == 'Tas Selempang Anak' : real_kategori = 1978
            elif kategori_c == 'Tas Koper Anak' : real_kategori = 1980
            elif kategori_c == 'Tas Backpack Anak' : real_kategori = 1979
            elif kategori_c == 'Gelang' : real_kategori = 2062
            elif kategori_c == 'Anting' : real_kategori = 2064
            elif kategori_c == 'Kalung' : real_kategori = 2061
            elif kategori_c == 'Cincin' : real_kategori = 2063
            elif kategori_c == 'Kacamata Anak' : real_kategori = 2058
            elif kategori_c == 'Jam Tangan Anak' : real_kategori = 2313
            elif kategori_c == 'Ikat Pinggang Anak' : real_kategori = 2056
            elif kategori_c == 'Dompet Anak' : real_kategori = 2055
            elif kategori_c == 'Topi Anak' : real_kategori = 2057
            elif kategori_c == 'Kaos Kaki' : real_kategori = 2053
            elif kategori_c == 'Sandal Jepit' : real_kategori = 2044
            elif kategori_c == 'Sepatu Sandal' : real_kategori = 2045
            elif kategori_c == 'Boots' : real_kategori = 1995
            elif kategori_c == 'Sepatu Kets' : real_kategori = 1996
            elif kategori_c == 'Sepatu Kets' : real_kategori = 1983
            elif kategori_c == 'Sandal Jepit' : real_kategori = 1981
            elif kategori_c == 'Kaos Kaki' : real_kategori = 1984
            elif kategori_c == 'Sepatu Sandal' : real_kategori = 1982
            elif kategori_c == 'Flat Shoes' : real_kategori = 1975
            elif kategori_c == 'Boots' : real_kategori = 1976
            elif kategori_c == 'Sepatu Pesta' : real_kategori = 2052
            elif kategori_c == 'Kaos' : real_kategori = 2071
            elif kategori_c == 'Celana Pendek' : real_kategori = 1600
            elif kategori_c == 'Baby Dolls' : real_kategori = 140
            elif kategori_c == 'Baju Setelan' : real_kategori = 141
            elif kategori_c == 'Blouse' : real_kategori = 142
            elif kategori_c == 'Bolero' : real_kategori = 143
            elif kategori_c == 'Cardigan' : real_kategori = 144
            elif kategori_c == 'Celana' : real_kategori = 145
            elif kategori_c == 'Dress' : real_kategori = 146
            elif kategori_c == 'Hoodies' : real_kategori = 147
            elif kategori_c == 'Jaket & Blazer' : real_kategori = 148
            elif kategori_c == 'Celana Jeans' : real_kategori = 149
            elif kategori_c == 'Jumpsuits' : real_kategori = 150
            elif kategori_c == 'Kemeja' : real_kategori = 151
            elif kategori_c == 'Kostum' : real_kategori = 152
            elif kategori_c == 'Legging' : real_kategori = 153
            elif kategori_c == 'Pakaian Dalam' : real_kategori = 155
            elif kategori_c == 'Baju Tidur Anak Perempuan' : real_kategori = 156
            elif kategori_c == 'Rok' : real_kategori = 157
            elif kategori_c == 'Seragam' : real_kategori = 158
            elif kategori_c == 'Tank Top' : real_kategori = 160
            elif kategori_c == 'Pakaian Anak Perempuan Lainnya' : real_kategori = 154
            elif kategori_c == 'Celana Pendek' : real_kategori = 1603
            elif kategori_c == 'Baju Setelan' : real_kategori = 161
            elif kategori_c == 'Kaos' : real_kategori = 2072
            elif kategori_c == 'Celana Panjang' : real_kategori = 162
            elif kategori_c == 'Hoodies' : real_kategori = 163
            elif kategori_c == 'Jaket & Blazer' : real_kategori = 164
            elif kategori_c == 'Celana Jeans' : real_kategori = 165
            elif kategori_c == 'Jumpsuits' : real_kategori = 166
            elif kategori_c == 'Kemeja' : real_kategori = 167
            elif kategori_c == 'Kostum' : real_kategori = 168
            elif kategori_c == 'Pakaian Dalam' : real_kategori = 170
            elif kategori_c == 'Baju Tidur Anak' : real_kategori = 171
            elif kategori_c == 'Seragam' : real_kategori = 172
            elif kategori_c == 'Pakaian Anak Laki-Laki Lainnya' : real_kategori = 169
            elif kategori_b == 'Handphone' : real_kategori = 24
            elif kategori_b == 'Power Bank' : real_kategori = 615
            elif kategori_b == 'Smartwatch' : real_kategori = 1536
            elif kategori_b == 'Tablet' : real_kategori = 276
            elif kategori_c == 'Baterai' : real_kategori = 67
            elif kategori_c == 'Aksesoris Mobil' : real_kategori = 68
            elif kategori_c == 'Casing & Cover' : real_kategori = 69
            elif kategori_c == 'Skin Handphone' : real_kategori = 599
            elif kategori_c == 'Charger' : real_kategori = 70
            elif kategori_c == 'Mount Handphone' : real_kategori = 73
            elif kategori_c == 'Gantungan Handphone' : real_kategori = 74
            elif kategori_c == 'Spare Part' : real_kategori = 75
            elif kategori_c == 'Screen Guard' : real_kategori = 76
            elif kategori_c == 'Docking Handphone' : real_kategori = 600
            elif kategori_c == 'Aksesoris Handphone Lainnya' : real_kategori = 77
            elif kategori_c == 'Baterai' : real_kategori = 278
            elif kategori_c == 'Aksesoris Mobil' : real_kategori = 279
            elif kategori_c == 'Casing & Cover' : real_kategori = 280
            elif kategori_c == 'Charger' : real_kategori = 281
            elif kategori_c == 'Mount Tablet' : real_kategori = 282
            elif kategori_c == 'Spare Part' : real_kategori = 285
            elif kategori_c == 'Screen Guard' : real_kategori = 286
            elif kategori_c == 'Keyboard Bluetooth' : real_kategori = 283
            elif kategori_c == 'Connection Kit' : real_kategori = 284
            elif kategori_c == 'Docking' : real_kategori = 601
            elif kategori_c == 'Aksesoris Tablet Lainnya' : real_kategori = 287
            elif kategori_c == 'Compact Flash' : real_kategori = 602
            elif kategori_c == 'Memory Stick PRO Duo' : real_kategori = 603
            elif kategori_c == 'Memory Stick PRO-HG Duo' : real_kategori = 604
            elif kategori_c == 'Memory Stick Micro M2' : real_kategori = 605
            elif kategori_c == 'MMC' : real_kategori = 606
            elif kategori_c == 'SD Card' : real_kategori = 607
            elif kategori_c == 'miniSD Card' : real_kategori = 608
            elif kategori_c == 'microSD Card' : real_kategori = 609
            elif kategori_c == 'Memory Card Lainnya' : real_kategori = 610
            elif kategori_b == 'Kabel Data' : real_kategori = 71
            elif kategori_b == 'Kabel & Konektor' : real_kategori = 616
            elif kategori_b == 'Headset Bluetooth' : real_kategori = 72
            elif kategori_b == 'Nomor Perdana & Voucher' : real_kategori = 275
            elif kategori_b == 'Stylus' : real_kategori = 360
            elif kategori_b == 'Lensa Handphone' : real_kategori = 1189
            elif kategori_b == 'Tongsis' : real_kategori = 1754
            elif kategori_b == 'Tomsis' : real_kategori = 1755
            elif kategori_b == 'Pelindung Kabel' : real_kategori = 1756
            elif kategori_b == 'Virtual Reality Glasses' : real_kategori = 1757
            elif kategori_c == 'Kapas Vape' : real_kategori = 2095
            elif kategori_c == 'Liquid' : real_kategori = 2096
            elif kategori_c == 'Aksesoris Vape' : real_kategori = 2092
            elif kategori_c == 'MOD' : real_kategori = 2097
            elif kategori_c == 'Atomizer' : real_kategori = 2091
            elif kategori_c == 'Coil' : real_kategori = 2094
            elif kategori_c == 'Earphone' : real_kategori = 565
            elif kategori_c == 'Speaker' : real_kategori = 562
            elif kategori_c == 'Headphone' : real_kategori = 564
            elif kategori_c == 'Headset' : real_kategori = 563
            elif kategori_c == 'Audio Lainnya' : real_kategori = 634
            elif kategori_c == 'LED TV' : real_kategori = 656
            elif kategori_c == 'LCD TV' : real_kategori = 657
            elif kategori_c == 'Plasma TV' : real_kategori = 658
            elif kategori_c == 'Remote TV' : real_kategori = 659
            elif kategori_c == 'Bracket' : real_kategori = 660
            elif kategori_c == 'Antena TV' : real_kategori = 661
            elif kategori_c == 'Kabel & Konektor' : real_kategori = 662
            elif kategori_c == 'TV Lainnya' : real_kategori = 663
            elif kategori_c == 'Alarm' : real_kategori = 561
            elif kategori_c == 'Paket Perangkat Keamanan' : real_kategori = 549
            elif kategori_c == 'Kamera CCTV' : real_kategori = 550
            elif kategori_c == 'IP Camera' : real_kategori = 551
            elif kategori_c == 'Fake Camera' : real_kategori = 552
            elif kategori_c == 'Spy Camera' : real_kategori = 553
            elif kategori_c == 'Wireless Camera' : real_kategori = 554
            elif kategori_c == 'DVR' : real_kategori = 664
            elif kategori_c == 'Spare Part' : real_kategori = 555
            elif kategori_c == 'Kamera Pengintai Lainnya' : real_kategori = 556
            elif kategori_c == 'MP3 Player' : real_kategori = 566
            elif kategori_c == 'MP4 Player' : real_kategori = 567
            elif kategori_c == 'DVD Player' : real_kategori = 568
            elif kategori_c == 'Receiver TV' : real_kategori = 665
            elif kategori_c == 'Media Player Lainnya' : real_kategori = 569
            elif kategori_c == 'Mesin Fax' : real_kategori = 570
            elif kategori_c == 'Telepon Kabel' : real_kategori = 571
            elif kategori_c == 'Telepon Wireless' : real_kategori = 572
            elif kategori_c == 'Telepon Satelit' : real_kategori = 666
            elif kategori_c == 'Telepon Lainnya' : real_kategori = 635
            elif kategori_b == 'Tool & Kit' : real_kategori = 636
            elif kategori_c == 'Bohlam' : real_kategori = 1024
            elif kategori_c == 'Senter' : real_kategori = 1025
            elif kategori_c == 'Lampu Baca' : real_kategori = 1026
            elif kategori_c == 'Lampu Meja' : real_kategori = 575
            elif kategori_c == 'Lampu Dinding' : real_kategori = 1261
            elif kategori_c == 'Lampu Gantung' : real_kategori = 1027
            elif kategori_c == 'Lampu Darurat' : real_kategori = 1028
            elif kategori_c == 'Lampu Proyektor' : real_kategori = 1029
            elif kategori_c == 'Pencahayaan Lainnya' : real_kategori = 1030
            elif kategori_c == 'Stop Kontak' : real_kategori = 1031
            elif kategori_c == 'Pengaman Stop Kontak' : real_kategori = 1267
            elif kategori_c == 'Saklar' : real_kategori = 1032
            elif kategori_c == 'Penghemat Listrik' : real_kategori = 1268
            elif kategori_c == 'Anti Petir' : real_kategori = 1269
            elif kategori_c == 'Alarm' : real_kategori = 1034
            elif kategori_c == 'Bel' : real_kategori = 1033
            elif kategori_c == 'Listrik Lainnya' : real_kategori = 1035
            elif kategori_c == 'Baterai' : real_kategori = 573
            elif kategori_c == 'Kipas Angin Listrik' : real_kategori = 667
            elif kategori_c == 'Stun Gun' : real_kategori = 576
            elif kategori_c == 'GPS' : real_kategori = 668
            elif kategori_c == 'Perangkat Elektronik Lainnya Lainnya' : real_kategori = 577
            elif kategori_c == 'Alat Potong Rambut' : real_kategori = 2254
            elif kategori_c == 'Aksesoris Rambut' : real_kategori = 2257
            elif kategori_c == 'Rambut Palsu' : real_kategori = 2250
            elif kategori_c == 'Produk Styling Rambut' : real_kategori = 2256
            elif kategori_c == 'Catokan' : real_kategori = 2253
            elif kategori_c == 'Hair Dryer' : real_kategori = 2252
            elif kategori_c == 'Sisir' : real_kategori = 2255
            elif kategori_c == 'Hair Extension' : real_kategori = 2251
            elif kategori_c == 'Eye Primer' : real_kategori = 2220
            elif kategori_c == 'Lem Bulu Mata' : real_kategori = 2223
            elif kategori_c == 'Bulu Mata Palsu' : real_kategori = 2222
            elif kategori_c == 'Mascara' : real_kategori = 2226
            elif kategori_c == 'Eye Liner' : real_kategori = 2219
            elif kategori_c == 'Eyelid Tape' : real_kategori = 2225
            elif kategori_c == 'Pinset & Penjepit Bulu Mata' : real_kategori = 2224
            elif kategori_c == 'Eyeshadow' : real_kategori = 2221
            elif kategori_c == 'Blush on' : real_kategori = 2210
            elif kategori_c == 'BB cream & CC cream, BB cushion' : real_kategori = 2209
            elif kategori_c == 'Bronzer & Highlighter' : real_kategori = 2214
            elif kategori_c == 'Setting Spray' : real_kategori = 2213
            elif kategori_c == 'Bedak Wajah' : real_kategori = 2211
            elif kategori_c == 'Face primer' : real_kategori = 2207
            elif kategori_c == 'Concealer' : real_kategori = 2212
            elif kategori_c == 'Foundation' : real_kategori = 2208
            elif kategori_c == 'Henna' : real_kategori = 2249
            elif kategori_c == 'Stiker Kuku' : real_kategori = 2244
            elif kategori_c == 'Alat & Aksesoris Nail art' : real_kategori = 2248
            elif kategori_c == 'Fake Nail' : real_kategori = 2245
            elif kategori_c == 'Kutek' : real_kategori = 2243
            elif kategori_c == 'Portable Nail Dryer' : real_kategori = 2247
            elif kategori_c == 'Lem Kuku Palsu' : real_kategori = 2246
            elif kategori_b == 'Set & Palette Makeup' : real_kategori = 2205
            elif kategori_c == 'Pensil Alis' : real_kategori = 2216
            elif kategori_c == 'Cetakan dan Sisir Alis' : real_kategori = 2218
            elif kategori_c == 'Eyebrow Powder & Pomade' : real_kategori = 2215
            elif kategori_c == 'Pinset dan Cukuran Alis' : real_kategori = 2217
            elif kategori_c == 'Tas Kosmetik' : real_kategori = 2236
            elif kategori_c == 'Set Makeup Brush' : real_kategori = 2233
            elif kategori_c == 'Pembersih Brush Make Up' : real_kategori = 2234
            elif kategori_c == 'Pinset Komedo' : real_kategori = 2241
            elif kategori_c == 'Laci & Tempat Makeup' : real_kategori = 2235
            elif kategori_c == 'Beauty Sponge' : real_kategori = 2239
            elif kategori_c == 'Kemasan Make Up' : real_kategori = 2240
            elif kategori_c == 'Cermin Make Up' : real_kategori = 2242
            elif kategori_c == 'Penghilang Bekas Jerawat' : real_kategori = 2260
            elif kategori_c == 'Penghilang Bekas Luka' : real_kategori = 2259
            elif kategori_c == 'Anti Selulit & Stretchmark' : real_kategori = 2258
            elif kategori_c == 'Lip Tint' : real_kategori = 2230
            elif kategori_c == 'Lipstik dan Pensil Bibir' : real_kategori = 2227
            elif kategori_c == 'Lip Balm & Oil' : real_kategori = 2231
            elif kategori_c == 'Lipgloss' : real_kategori = 2229
            elif kategori_c == 'Lip Scrub' : real_kategori = 2232
            elif kategori_c == 'Lip Cream' : real_kategori = 2228
            elif kategori_c == 'Cleanser' : real_kategori = 2266
            elif kategori_c == 'Serum & Masker Mata' : real_kategori = 2263
            elif kategori_c == 'Krim Mata' : real_kategori = 2262
            elif kategori_c == 'Skin Care Tools' : real_kategori = 2268
            elif kategori_c == 'Serum & Minyak Wajah' : real_kategori = 2265
            elif kategori_c == 'Masker Bibir' : real_kategori = 2264
            elif kategori_c == 'Pembersih Make Up' : real_kategori = 2267
            elif kategori_c == 'Scrub & Peeling Wajah' : real_kategori = 2269
            elif kategori_c == 'Krim Wajah' : real_kategori = 2261
            elif kategori_c == 'Masker Wajah' : real_kategori = 418
            elif kategori_c == 'Sunblock Wajah' : real_kategori = 421
            elif kategori_c == 'Toner' : real_kategori = 512
            elif kategori_c == 'Paket Perawatan Wajah' : real_kategori = 425
            elif kategori_c == 'Obat Batuk dan Pilek' : real_kategori = 2292
            elif kategori_c == 'Obat Penumbuh Rambut' : real_kategori = 2294
            elif kategori_c == 'Obat Jerawat' : real_kategori = 2295
            elif kategori_c == 'Obat Pencernaan' : real_kategori = 2296
            elif kategori_c == 'Obat Sakit Kepala dan Demam' : real_kategori = 2293
            elif kategori_c == 'Obat Diabetes' : real_kategori = 2291
            elif kategori_c == 'Obat Generik' : real_kategori = 2290
            elif kategori_c == 'Obat Lainnya' : real_kategori = 2301
            elif kategori_c == 'Koyo' : real_kategori = 2298
            elif kategori_c == 'Obat Herbal' : real_kategori = 2289
            elif kategori_c == 'Salep' : real_kategori = 2297
            elif kategori_c == 'Vitamin Ibu Hamil' : real_kategori = 2274
            elif kategori_c == 'Nipple Cream' : real_kategori = 2275
            elif kategori_c == 'Susu Hamil' : real_kategori = 2276
            elif kategori_c == 'Kehamilan' : real_kategori = 2309
            elif kategori_c == 'Asi Booster' : real_kategori = 2273
            elif kategori_c == 'Alat Pelangsing' : real_kategori = 2284
            elif kategori_c == 'Termometer' : real_kategori = 2288
            elif kategori_c == 'Behel' : real_kategori = 2283
            elif kategori_c == 'Kacamata Terapi' : real_kategori = 2282
            elif kategori_c == 'Alat Bantu Pendengaran' : real_kategori = 2280
            elif kategori_c == 'Peralatan P3K' : real_kategori = 2286
            elif kategori_c == 'Timbangan Badan' : real_kategori = 2285
            elif kategori_c == 'Alat Pijat' : real_kategori = 2287
            elif kategori_c == 'Earmuff' : real_kategori = 2281
            elif kategori_b == 'Essential Oil' : real_kategori = 2272
            elif kategori_c == 'Obat Menstruasi' : real_kategori = 2300
            elif kategori_c == 'Perawatan Tubuh Wanita' : real_kategori = 521
            elif kategori_c == 'Alat Kontrasepsi' : real_kategori = 717
            elif kategori_c == 'Produk Kesehatan Wanita' : real_kategori = 903
            elif kategori_c == 'Obat Menopause' : real_kategori = 719
            elif kategori_c == 'Kesehatan Wanita Lainnya' : real_kategori = 722
            elif kategori_c == 'Detox' : real_kategori = 467
            elif kategori_c == 'Obat Pelangsing' : real_kategori = 2312
            elif kategori_c == 'Suplemen Fitness' : real_kategori = 743
            elif kategori_c == 'Vitamin & Nutrisi' : real_kategori = 469
            elif kategori_c == 'Penambah Berat Badan' : real_kategori = 744
            elif kategori_c == 'Vitamin Daya Tahan Tubuh' : real_kategori = 726
            elif kategori_c == 'Diet & Vitamin Lainnya' : real_kategori = 745
            elif kategori_c == 'Alat Diagnosa' : real_kategori = 2310
            elif kategori_c == 'Alat Terapi' : real_kategori = 1745
            elif kategori_c == 'Alat Lainnya' : real_kategori = 2299
            elif kategori_c == 'Alat Monitor Kesehatan' : real_kategori = 2311
            elif kategori_c == 'Alat Bantu Jalan' : real_kategori = 1747
            elif kategori_c == 'Alat Laboratorium' : real_kategori = 1751
            elif kategori_b == 'Kesehatan Lainnya' : real_kategori = 1129
            elif kategori_c == 'Diaper' : real_kategori = 2042
            elif kategori_c == 'Popok Kain' : real_kategori = 2041
            elif kategori_c == 'Biskuit Bayi' : real_kategori = 2011
            elif kategori_c == 'Susu Bayi' : real_kategori = 394
            elif kategori_c == 'Bubur Bayi' : real_kategori = 395
            elif kategori_c == 'Makanan & Susu Bayi Lainnya' : real_kategori = 396
            elif kategori_c == 'Jumper Bayi' : real_kategori = 1732
            elif kategori_c == 'Jaket Bayi' : real_kategori = 1733
            elif kategori_c == 'Baju Bayi Perempuan' : real_kategori = 379
            elif kategori_c == 'Baju Bayi Laki-laki' : real_kategori = 380
            elif kategori_c == 'Pakaian Bayi Unisex' : real_kategori = 401
            elif kategori_c == 'Sepatu' : real_kategori = 381
            elif kategori_c == 'Sarung Tangan & Kaos Kaki' : real_kategori = 383
            elif kategori_c == 'Baju & Sepatu Bayi Lainnya' : real_kategori = 384
            elif kategori_c == 'Cream Bayi' : real_kategori = 2030
            elif kategori_c == 'Kesehatan Bayi' : real_kategori = 2032
            elif kategori_c == 'Kapas dan Tissue' : real_kategori = 2031
            elif kategori_c == 'Bedak Bayi' : real_kategori = 2029
            elif kategori_c == 'Minyak Telon' : real_kategori = 2028
            elif kategori_c == 'Botol Susu Sanitizer' : real_kategori = 2010
            elif kategori_c == 'Botol Susu' : real_kategori = 2008
            elif kategori_c == 'Kursi Makan Bayi' : real_kategori = 2069
            elif kategori_c == 'Baby Food Maker' : real_kategori = 2070
            elif kategori_c == 'Set Peralatan Makan Bayi' : real_kategori = 2007
            elif kategori_c == 'Celemek Bayi' : real_kategori = 2006
            elif kategori_c == 'Dot' : real_kategori = 2009
            elif kategori_c == 'Pelampung' : real_kategori = 2023
            elif kategori_c == 'Mainan Mandi' : real_kategori = 2024
            elif kategori_c == 'Bathub dan Kolam' : real_kategori = 2022
            elif kategori_c == 'Topi Pelindung Air' : real_kategori = 2025
            elif kategori_c == 'Shampoo Bayi' : real_kategori = 2020
            elif kategori_c == 'Handuk dan Peralatan Mandi' : real_kategori = 2043
            elif kategori_c == 'Sabun Bayi' : real_kategori = 2021
            elif kategori_c == 'Pispot' : real_kategori = 2026
            elif kategori_c == 'Gendongan Bayi' : real_kategori = 2014
            elif kategori_c == 'Dudukan Mobil Bayi' : real_kategori = 2016
            elif kategori_c == 'Stroller' : real_kategori = 2013
            elif kategori_b == 'Tas Perlengkapan Bayi' : real_kategori = 2017
            elif kategori_c == 'Tempat Tidur Bayi' : real_kategori = 2034
            elif kategori_c == 'Bantal dan Guling' : real_kategori = 2035
            elif kategori_c == 'Baby Monitor' : real_kategori = 2038
            elif kategori_c == 'Selimut dan Bedong' : real_kategori = 2036
            elif kategori_c == 'Kelambu' : real_kategori = 2037
            elif kategori_c == 'Perhiasan Bayi' : real_kategori = 2000
            elif kategori_c == 'Headband Bayi' : real_kategori = 1999
            elif kategori_c == 'Topi Bayi' : real_kategori = 1998
            elif kategori_c == 'Rok Hamil' : real_kategori = 1989
            elif kategori_c == 'Dress Hamil' : real_kategori = 1986
            elif kategori_c == 'Baju Atasan Hamil' : real_kategori = 1987
            elif kategori_c == 'Celana Dalam Hamil' : real_kategori = 1991
            elif kategori_c == 'Korset Ibu Hamil' : real_kategori = 1993
            elif kategori_c == 'Apron Menyusui' : real_kategori = 2085
            elif kategori_c == 'Gurita' : real_kategori = 1992
            elif kategori_c == 'Bra Menyusui' : real_kategori = 1990
            elif kategori_c == 'Celana Hamil' : real_kategori = 1988
            elif kategori_c == 'Vitamin & Nutrisi Ibu Hamil' : real_kategori = 2089
            elif kategori_c == 'Susu Ibu Hamil' : real_kategori = 2314
            elif kategori_c == 'ASI Booster' : real_kategori = 2087
            elif kategori_c == 'Nipple Cream' : real_kategori = 2123
            elif kategori_b == 'Breast Pump' : real_kategori = 2039
            elif kategori_c == 'Playmat' : real_kategori = 2002
            elif kategori_c == 'bouncer' : real_kategori = 2004
            elif kategori_c == 'Mainan Luar Ruang' : real_kategori = 2346
            elif kategori_c == 'Mainan Edukasi' : real_kategori = 2068
            elif kategori_c == 'Mainan Gigi' : real_kategori = 2003
            elif kategori_b == 'Alat Bantu Jalan Bayi' : real_kategori = 2018
            elif kategori_c == 'Hair Foam' : real_kategori = 2196
            elif kategori_c == 'Alat & Krim Cukur' : real_kategori = 2195
            elif kategori_c == 'Sisir Saku' : real_kategori = 2194
            elif kategori_c == 'Hair Wax & Pomade' : real_kategori = 2193
            elif kategori_c == 'Parfum & Cologne Unisex' : real_kategori = 2191
            elif kategori_c == 'Parfum & Cologne Wanita' : real_kategori = 2189
            elif kategori_c == 'Parfum & Cologne Anak-Anak' : real_kategori = 2192
            elif kategori_c == 'Parfum & Cologne Pria' : real_kategori = 2190
            elif kategori_c == 'Ear Candle' : real_kategori = 2178
            elif kategori_c == 'Pembersih Telinga' : real_kategori = 2179
            elif kategori_c == 'Tampon' : real_kategori = 2308
            elif kategori_c == 'Sabun Kewanitaan' : real_kategori = 2170
            elif kategori_c == 'Pembalut' : real_kategori = 2169
            elif kategori_c == 'Shampoo' : real_kategori = 2174
            elif kategori_c == 'Pewarna Rambut' : real_kategori = 2173
            elif kategori_c == 'Hair tonic' : real_kategori = 2177
            elif kategori_c == 'Masker Rambut' : real_kategori = 2171
            elif kategori_c == 'Conditioner' : real_kategori = 2176
            elif kategori_c == 'Minyak & Serum Rambut' : real_kategori = 2172
            elif kategori_c == 'Dry Shampoo' : real_kategori = 2175
            elif kategori_c == 'Tetes Mata' : real_kategori = 2154
            elif kategori_c == 'Softlens' : real_kategori = 2152
            elif kategori_c == 'Cairan Pembersih Sofltens' : real_kategori = 2153
            elif kategori_c == 'Pemutih Ketiak' : real_kategori = 2144
            elif kategori_c == 'Paket Perawatan & Perlengkapan Mandi' : real_kategori = 2142
            elif kategori_c == 'Sunblock Badan' : real_kategori = 2141
            elif kategori_c == 'Deodorant' : real_kategori = 2140
            elif kategori_c == 'Body Lotion' : real_kategori = 2136
            elif kategori_c == 'Body Butter' : real_kategori = 2137
            elif kategori_c == 'Sabun Badan' : real_kategori = 2139
            elif kategori_c == 'Body Scrub' : real_kategori = 2138
            elif kategori_c == 'Perontok Bulu' : real_kategori = 2143
            elif kategori_c == 'Minyak Kutikula Kuku' : real_kategori = 2180
            elif kategori_c == 'Hand Sanitizer' : real_kategori = 2184
            elif kategori_c == 'Perawatan Kaki' : real_kategori = 2186
            elif kategori_c == 'Sabun Cuci Tangan' : real_kategori = 2187
            elif kategori_c == 'Paket Perawatan Tangan & Kaki' : real_kategori = 2188
            elif kategori_c == 'Penghilang Cat Kuku' : real_kategori = 2181
            elif kategori_c == 'Alat Manikur & Pedikur' : real_kategori = 2183
            elif kategori_c == 'Gunting Kuku' : real_kategori = 2182
            elif kategori_c == 'Hand Cream' : real_kategori = 2185
            elif kategori_c == 'Pembersih Lidah' : real_kategori = 2165
            elif kategori_c == 'Benang Gigi & Tusuk Gigi' : real_kategori = 2168
            elif kategori_c == 'Obat Kumur' : real_kategori = 2163
            elif kategori_c == 'Sikat Gigi' : real_kategori = 2166
            elif kategori_c == 'Pasta Gigi' : real_kategori = 2164
            elif kategori_c == 'Pemutih Gigi' : real_kategori = 2167
            elif kategori_c == 'Tempat Tidur' : real_kategori = 996
            elif kategori_c == 'Mattress Cover' : real_kategori = 1367
            elif kategori_c == 'Bantal Kepala & Leher' : real_kategori = 997
            elif kategori_c == 'Bantal Guling' : real_kategori = 998
            elif kategori_c == 'Sprei & Bed Cover' : real_kategori = 999
            elif kategori_c == 'Selimut' : real_kategori = 1000
            elif kategori_c == 'Sarung Bantal' : real_kategori = 1259
            elif kategori_c == 'Kamar Tidur Lainnya' : real_kategori = 1001
            elif kategori_c == 'Handuk & Kimono Mandi' : real_kategori = 1002
            elif kategori_c == 'Gantungan Handuk' : real_kategori = 1003
            elif kategori_c == 'Gayung' : real_kategori = 1004
            elif kategori_c == 'Ember & Baskom' : real_kategori = 1005
            elif kategori_c == 'Tempat Sabun' : real_kategori = 1006
            elif kategori_c == 'Tempat Sikat Gigi' : real_kategori = 1007
            elif kategori_c == 'Dispenser Odol' : real_kategori = 1131
            elif kategori_c == 'Shower Curtain' : real_kategori = 1008
            elif kategori_c == 'Toilet Cover' : real_kategori = 1260
            elif kategori_c == 'Kamar Mandi Lainnya' : real_kategori = 1009
            elif kategori_c == 'Setrika' : real_kategori = 1010
            elif kategori_c == 'Gantungan Baju' : real_kategori = 1011
            elif kategori_c == 'Jemuran Baju' : real_kategori = 1012
            elif kategori_c == 'Laundry Bag' : real_kategori = 1013
            elif kategori_c == 'Laundry Lainnya' : real_kategori = 1014
            elif kategori_c == 'Vacuum Cleaners' : real_kategori = 1015
            elif kategori_c == 'Kemoceng' : real_kategori = 1016
            elif kategori_c == 'Sikat' : real_kategori = 1017
            elif kategori_c == 'Kain Lap' : real_kategori = 1018
            elif kategori_c == 'Sapu' : real_kategori = 1019
            elif kategori_c == 'Alat Pel' : real_kategori = 1020
            elif kategori_c == 'Tempat Sampah' : real_kategori = 1021
            elif kategori_c == 'Pengharum Ruangan' : real_kategori = 1022
            elif kategori_c == 'Pest Control' : real_kategori = 1069
            elif kategori_c == 'Kebersihan Lainnya' : real_kategori = 1023
            elif kategori_c == 'Keran Air' : real_kategori = 1263
            elif kategori_c == 'Filter Keran Air' : real_kategori = 1067
            elif kategori_c == 'Pompa Air' : real_kategori = 1264
            elif kategori_c == 'Pembersih Saluran Air' : real_kategori = 1265
            elif kategori_c == 'Ledeng Lainnya' : real_kategori = 1266
            elif kategori_c == 'Botol' : real_kategori = 1037
            elif kategori_c == 'Kotak' : real_kategori = 1038
            elif kategori_c == 'Keranjang' : real_kategori = 1039
            elif kategori_c == 'Laci' : real_kategori = 1044
            elif kategori_c == 'Tempat Pakaian' : real_kategori = 1368
            elif kategori_c == 'Tempat Perhiasan & Aksesoris' : real_kategori = 1369
            elif kategori_c == 'Tempat Jam' : real_kategori = 1370
            elif kategori_c == 'Tempat Tas' : real_kategori = 1371
            elif kategori_c == 'Tempat Sepatu & Sandal' : real_kategori = 1372
            elif kategori_c == 'Tempat Tissue' : real_kategori = 1040
            elif kategori_c == 'Tempat Obat' : real_kategori = 1373
            elif kategori_c == 'Travel Organizer' : real_kategori = 1374
            elif kategori_c == 'Tempat Penyimpanan Lainnya' : real_kategori = 1041
            elif kategori_c == 'Meja' : real_kategori = 1042
            elif kategori_c == 'Kursi & Sofa' : real_kategori = 1043
            elif kategori_c == 'Lemari' : real_kategori = 1045
            elif kategori_c == 'Rak' : real_kategori = 1270
            elif kategori_c == 'Pengaman Furniture' : real_kategori = 1068
            elif kategori_c == 'Furniture Lainnya' : real_kategori = 1047
            elif kategori_c == 'Jam Meja' : real_kategori = 638
            elif kategori_c == 'Jam Dinding' : real_kategori = 1048
            elif kategori_c == 'Patung' : real_kategori = 1049
            elif kategori_c == 'Bunga Artelificial' : real_kategori = 1271
            elif kategori_c == 'Vas Bunga' : real_kategori = 1272
            elif kategori_c == 'Lilin' : real_kategori = 1273
            elif kategori_c == 'Tempat Lilin' : real_kategori = 1274
            elif kategori_c == 'Taplak Meja' : real_kategori = 978
            elif kategori_c == 'Lukisan' : real_kategori = 1050
            elif kategori_c == 'Wallpaper' : real_kategori = 1051
            elif kategori_c == 'Wall Sticker' : real_kategori = 1052
            elif kategori_c == 'Karpet & Tikar' : real_kategori = 1053
            elif kategori_c == 'Keset' : real_kategori = 1054
            elif kategori_c == 'Gorden' : real_kategori = 1055
            elif kategori_c == 'Dekorasi Lainnya' : real_kategori = 1056
            elif kategori_c == 'Obeng' : real_kategori = 1057
            elif kategori_c == 'Palu' : real_kategori = 1058
            elif kategori_c == 'Tang' : real_kategori = 1059
            elif kategori_c == 'Kunci Inggris' : real_kategori = 1060
            elif kategori_c == 'Kunci L' : real_kategori = 1061
            elif kategori_c == 'Bor' : real_kategori = 1062
            elif kategori_c == 'Gergaji' : real_kategori = 1063
            elif kategori_c == 'Tool Box' : real_kategori = 1064
            elif kategori_c == 'Meteran' : real_kategori = 1073
            elif kategori_c == 'Pompa Angin' : real_kategori = 1074
            elif kategori_c == 'Lem Material' : real_kategori = 1275
            elif kategori_c == 'Blow Torch' : real_kategori = 1070
            elif kategori_c == 'Gembok' : real_kategori = 1066
            elif kategori_c == 'Alat Pertukangan Lainnya' : real_kategori = 1065
            elif kategori_c == 'Pupuk' : real_kategori = 1657
            elif kategori_c == 'Benih Bibit Tanaman' : real_kategori = 1655
            elif kategori_c == 'Peralatan Berkebun' : real_kategori = 1658
            elif kategori_c == 'Hiasan Taman' : real_kategori = 1659
            elif kategori_c == 'Irigasi' : real_kategori = 1752
            elif kategori_c == 'Media Tanam' : real_kategori = 1753
            elif kategori_c == 'Pot Tanaman' : real_kategori = 1656
            elif kategori_c == 'Obat Hewan' : real_kategori = 1662
            elif kategori_c == 'Grooming Hewan' : real_kategori = 1663
            elif kategori_c == 'Kandang Hewan' : real_kategori = 1664
            elif kategori_c == 'Mainan Hewan' : real_kategori = 1665
            elif kategori_c == 'Aksesoris Hewan' : real_kategori = 1666
            elif kategori_c == 'Baju Hewan' : real_kategori = 1734
            elif kategori_c == 'Aquarium' : real_kategori = 1735
            elif kategori_c == 'Hiasan Aquarium' : real_kategori = 1736
            elif kategori_c == 'Aksesoris Aquarium' : real_kategori = 1737
            elif kategori_c == 'Tempat Tidur Hewan' : real_kategori = 1738
            elif kategori_c == 'Makanan Hewan' : real_kategori = 1661
            elif kategori_b == 'Rumah Tangga Lainnya' : real_kategori = 995
            elif kategori_c == 'Aksesoris Game Console' : real_kategori = 2131
            elif kategori_c == 'Komponen Game Console' : real_kategori = 2107
            elif kategori_c == 'Wheels' : real_kategori = 2106
            elif kategori_c == 'Game Boy dan Game Retro' : real_kategori = 2104
            elif kategori_c == 'Joystick' : real_kategori = 2105
            elif kategori_c == 'Nintendo' : real_kategori = 2102
            elif kategori_c == 'PlayStation' : real_kategori = 2101
            elif kategori_c == 'Memory Card' : real_kategori = 2128
            elif kategori_c == 'Xbox' : real_kategori = 2103
            elif kategori_c == 'CD PlayStation' : real_kategori = 2118
            elif kategori_c == 'CD Nintendo' : real_kategori = 2119
            elif kategori_c == 'CD Xbox' : real_kategori = 2120
            elif kategori_c == 'CD PC dan Laptop Gaming' : real_kategori = 2121
            elif kategori_c == 'Komponen Komputer' : real_kategori = 2127
            elif kategori_c == 'Mouse Gaming' : real_kategori = 2112
            elif kategori_c == 'Laptop Gaming' : real_kategori = 2111
            elif kategori_c == 'PC Gaming' : real_kategori = 2110
            elif kategori_c == 'Mouse & Keyboard Gaming Bundle' : real_kategori = 2129
            elif kategori_c == 'Aksesoris PC Gaming' : real_kategori = 2116
            elif kategori_c == 'PC Controller' : real_kategori = 2115
            elif kategori_c == 'Keyboard Gaming' : real_kategori = 2113
            elif kategori_c == 'Virtual Reality Glasses' : real_kategori = 2124
            elif kategori_c == 'Headset Gaming' : real_kategori = 2114
            elif kategori_c == 'Monitor' : real_kategori = 2126
            elif kategori_b == 'Laptop' : real_kategori = 289
            elif kategori_c == 'Memory RAM' : real_kategori = 291
            elif kategori_c == 'Cooling Pad' : real_kategori = 292
            elif kategori_c == 'Baterai Laptop' : real_kategori = 293
            elif kategori_c == 'Adaptor Laptop' : real_kategori = 294
            elif kategori_c == 'Protector' : real_kategori = 295
            elif kategori_c == 'Skin Laptop' : real_kategori = 557
            elif kategori_c == 'Meja Laptop' : real_kategori = 558
            elif kategori_c == 'Tas Laptop' : real_kategori = 217
            elif kategori_c == 'Spare Part Laptop' : real_kategori = 559
            elif kategori_c == 'Aksesoris Laptop Lainnya' : real_kategori = 296
            elif kategori_b == 'Desktop & Mini PC' : real_kategori = 298
            elif kategori_c == 'HDD External' : real_kategori = 321
            elif kategori_c == 'HDD Internal' : real_kategori = 322
            elif kategori_c == 'SSD' : real_kategori = 323
            elif kategori_c == 'Flash Disk' : real_kategori = 342
            elif kategori_c == 'HDD Cases & Docking' : real_kategori = 363
            elif kategori_c == 'Storage Lainnya' : real_kategori = 345
            elif kategori_c == 'NVIDIA Series - Geforce' : real_kategori = 318
            elif kategori_c == 'AMD Series - ATI' : real_kategori = 319
            elif kategori_c == 'AGP Series' : real_kategori = 362
            elif kategori_c == 'All in One' : real_kategori = 325
            elif kategori_c == 'Dot Matrix' : real_kategori = 326
            elif kategori_c == 'Ink Jet' : real_kategori = 327
            elif kategori_c == 'Laser Color' : real_kategori = 328
            elif kategori_c == 'Laser Mono' : real_kategori = 329
            elif kategori_c == 'Point of Sales (POS)' : real_kategori = 331
            elif kategori_c == 'Barcode' : real_kategori = 353
            elif kategori_c == 'Tinta Printer' : real_kategori = 354
            elif kategori_c == 'Kertas Printer' : real_kategori = 364
            elif kategori_c == 'Spare Part' : real_kategori = 365
            elif kategori_c == 'Printer Lainnya' : real_kategori = 355
            elif kategori_c == 'Mouse' : real_kategori = 339
            elif kategori_c == 'Keyboard' : real_kategori = 340
            elif kategori_c == 'Mouse & Keyboard Bundle' : real_kategori = 613
            elif kategori_c == 'Mousepad' : real_kategori = 350
            elif kategori_c == 'Keypad' : real_kategori = 614
            elif kategori_c == 'Card Readers' : real_kategori = 352
            elif kategori_c == 'Joystick & Wheel' : real_kategori = 373
            elif kategori_c == 'Scanner' : real_kategori = 341
            elif kategori_c == 'USB Hub' : real_kategori = 343
            elif kategori_c == 'Webcam' : real_kategori = 346
            elif kategori_c == 'CD & DVD Kosong' : real_kategori = 357
            elif kategori_c == 'Proyektor & Perangkat Presentasi' : real_kategori = 374
            elif kategori_c == 'TV Card & Tuner' : real_kategori = 375
            elif kategori_c == 'Kabel & Konektor' : real_kategori = 344
            elif kategori_c == 'Tools & Kits' : real_kategori = 376
            elif kategori_c == 'Peripheral & Aksesoris Lainnya' : real_kategori = 347
            elif kategori_c == 'Modem USB' : real_kategori = 333
            elif kategori_c == 'Wireless Router' : real_kategori = 334
            elif kategori_c == 'Wired Router' : real_kategori = 366
            elif kategori_c == 'Wireless Adapter' : real_kategori = 335
            elif kategori_c == 'Switch Internet' : real_kategori = 336
            elif kategori_c == 'Power Over Ethernet' : real_kategori = 378
            elif kategori_c == 'Powerline' : real_kategori = 367
            elif kategori_c == 'KVM Switch' : real_kategori = 368
            elif kategori_c == 'Network Transceiver' : real_kategori = 369
            elif kategori_c == 'Network Card' : real_kategori = 370
            elif kategori_c == 'Print Server' : real_kategori = 371
            elif kategori_c == 'Antena Penguat Sinyal' : real_kategori = 372
            elif kategori_c == 'Kabel & Konektor' : real_kategori = 337
            elif kategori_c == 'Networking Lainnya' : real_kategori = 356
            elif kategori_c == 'Processor Intel' : real_kategori = 300
            elif kategori_c == 'Processor AMD' : real_kategori = 301
            elif kategori_c == 'Motherboard Intel' : real_kategori = 302
            elif kategori_c == 'Motherboard AMD' : real_kategori = 303
            elif kategori_c == 'Memory' : real_kategori = 304
            elif kategori_c == 'Monitor' : real_kategori = 305
            elif kategori_c == 'Power Supply Unit (PSU)' : real_kategori = 306
            elif kategori_c == 'Casing Komputer' : real_kategori = 307
            elif kategori_c == 'Sound Card' : real_kategori = 308
            elif kategori_c == 'UPS' : real_kategori = 309
            elif kategori_c == 'Stabilizer' : real_kategori = 611
            elif kategori_c == 'CPU Cooler' : real_kategori = 310
            elif kategori_c == 'VGA Cooler' : real_kategori = 311
            elif kategori_c == 'Memory Cooler' : real_kategori = 348
            elif kategori_c == 'Harddisk Cooler' : real_kategori = 349
            elif kategori_c == 'Fan Case' : real_kategori = 312
            elif kategori_c == 'Thermal Paste' : real_kategori = 612
            elif kategori_c == 'CD' : real_kategori = 314
            elif kategori_c == 'DVD' : real_kategori = 315
            elif kategori_c == 'Blu-ray' : real_kategori = 316
            elif kategori_c == 'Duplicator' : real_kategori = 361
            elif kategori_c == 'Kamera DSLR' : real_kategori = 2324
            elif kategori_c == 'Kamera Mirrorless' : real_kategori = 2326
            elif kategori_c == 'Action Camera' : real_kategori = 2325
            elif kategori_c == 'Kamera Digital Lainnya' : real_kategori = 2327
            elif kategori_c == 'Kamera Pocket - Prosumer' : real_kategori = 2323
            elif kategori_c == 'Kamera Video Lainnya' : real_kategori = 2331
            elif kategori_c == 'Drone' : real_kategori = 2330
            elif kategori_c == 'Camcorder' : real_kategori = 2329
            elif kategori_c == 'Lomo' : real_kategori = 2332
            elif kategori_c == 'Kamera Analog Lainnya' : real_kategori = 2334
            elif kategori_c == 'Kamera Instan' : real_kategori = 2333
            elif kategori_c == 'Lensa' : real_kategori = 580
            elif kategori_c == 'Filter' : real_kategori = 589
            elif kategori_c == 'Cap' : real_kategori = 621
            elif kategori_c == 'Hood' : real_kategori = 622
            elif kategori_c == 'Adapter' : real_kategori = 671
            elif kategori_c == 'Converter - Teleconverter' : real_kategori = 672
            elif kategori_c == 'Lensa & Aksesoris Lainnya' : real_kategori = 623
            elif kategori_c == 'Flash' : real_kategori = 624
            elif kategori_c == 'Flash Trigger' : real_kategori = 674
            elif kategori_c == 'Deliffuser' : real_kategori = 675
            elif kategori_c == 'Hot Shoe' : real_kategori = 676
            elif kategori_c == 'Flash & Aksesoris Lainnya' : real_kategori = 678
            elif kategori_c == 'Tripod & Stabillizer' : real_kategori = 592
            elif kategori_c == 'Tas & Casing Kamera' : real_kategori = 593
            elif kategori_c == 'Waterproof Case' : real_kategori = 627
            elif kategori_c == 'Strap Kamera' : real_kategori = 591
            elif kategori_c == 'Lighting & Studio' : real_kategori = 626
            elif kategori_c == 'Remote - Wireless' : real_kategori = 708
            elif kategori_c == 'Kabel Konektor' : real_kategori = 709
            elif kategori_c == 'Memory Card Kamera' : real_kategori = 1188
            elif kategori_c == 'Aksesoris Kamera Lainnya' : real_kategori = 596
            elif kategori_c == 'Baterai' : real_kategori = 590
            elif kategori_c == 'Charger' : real_kategori = 687
            elif kategori_c == 'Battery Grip' : real_kategori = 688
            elif kategori_c == 'Baterai, Charger & Grip Lainnya' : real_kategori = 689
            elif kategori_c == 'Cleaning Kit' : real_kategori = 701
            elif kategori_c == 'Lenspen' : real_kategori = 702
            elif kategori_c == 'Blower' : real_kategori = 703
            elif kategori_c == 'Cleaning Cloth' : real_kategori = 704
            elif kategori_c == 'Dry Box' : real_kategori = 705
            elif kategori_c == 'Silica Gel' : real_kategori = 706
            elif kategori_c == 'Cleaner & Tool Kit Lainnya' : real_kategori = 707
            elif kategori_c == 'Frame Foto' : real_kategori = 2338
            elif kategori_c == 'Roll Film' : real_kategori = 2335
            elif kategori_c == 'Printer Foto' : real_kategori = 2337
            elif kategori_c == 'Frame Digital' : real_kategori = 2340
            elif kategori_c == 'Album' : real_kategori = 2339
            elif kategori_c == 'DVs' : real_kategori = 2336
            elif kategori_c == 'Parfum Mobil' : real_kategori = 1293
            elif kategori_c == 'Knalpot' : real_kategori = 1294
            elif kategori_c == 'Interior' : real_kategori = 1295
            elif kategori_c == 'Eksterior' : real_kategori = 1296
            elif kategori_c == 'Wheels' : real_kategori = 1297
            elif kategori_c == 'Klakson' : real_kategori = 1363
            elif kategori_c == 'Audio Mobil' : real_kategori = 1298
            elif kategori_c == 'Cover Mobil' : real_kategori = 1353
            elif kategori_c == 'Lampu' : real_kategori = 1299
            elif kategori_c == 'Aksesoris Mobil Lainnya' : real_kategori = 1300
            elif kategori_c == 'Baut-baut' : real_kategori = 1301
            elif kategori_c == 'Knalpot' : real_kategori = 1302
            elif kategori_c == 'Shockbreaker' : real_kategori = 1303
            elif kategori_c == 'Aksesori Body' : real_kategori = 1304
            elif kategori_c == 'Spion' : real_kategori = 1357
            elif kategori_c == 'Handle - Handfat' : real_kategori = 1356
            elif kategori_c == 'Klakson' : real_kategori = 1364
            elif kategori_c == 'Alarm & Gembok Motor' : real_kategori = 1365
            elif kategori_c == 'Footstep' : real_kategori = 1358
            elif kategori_c == 'Jok Motor' : real_kategori = 1305
            elif kategori_c == 'Cover Motor' : real_kategori = 1354
            elif kategori_c == 'Lampu' : real_kategori = 1306
            elif kategori_c == 'Box Motor' : real_kategori = 1307
            elif kategori_c == 'Ban dan Velg' : real_kategori = 1308
            elif kategori_c == 'Aksesoris Motor Lainnya' : real_kategori = 1309
            elif kategori_c == 'Full Face' : real_kategori = 1311
            elif kategori_c == 'Half Face' : real_kategori = 1312
            elif kategori_c == 'Kaca Helm' : real_kategori = 1313
            elif kategori_c == 'Kunci Helm' : real_kategori = 1314
            elif kategori_c == 'Tas & Jaring Helm' : real_kategori = 1376
            elif kategori_c == 'Helm Motor Lainnya' : real_kategori = 1315
            elif kategori_c == 'Rompi' : real_kategori = 1380
            elif kategori_c == 'Jaket' : real_kategori = 1317
            elif kategori_c == 'Jas Hujan' : real_kategori = 1318
            elif kategori_c == 'Sarung Tangan' : real_kategori = 1319
            elif kategori_c == 'Masker Motor' : real_kategori = 1320
            elif kategori_c == 'Sepatu' : real_kategori = 1375
            elif kategori_c == 'Aksesoris Pengendara Motor Lainnya' : real_kategori = 1321
            elif kategori_b == 'Sepeda Motor' : real_kategori = 2197
            elif kategori_b == 'Mobil' : real_kategori = 2344
            elif kategori_c == 'Anti Ban Bocor' : real_kategori = 1327
            elif kategori_c == 'Wash and Wax' : real_kategori = 1330
            elif kategori_c == 'Semir Ban' : real_kategori = 1331
            elif kategori_c == 'Lap Chamois' : real_kategori = 1332
            elif kategori_c == 'Pelumas Rantai' : real_kategori = 1366
            elif kategori_c == 'Perawatan Kendaraan Lainnya' : real_kategori = 1333
            elif kategori_c == 'Oli Mobil' : real_kategori = 1323
            elif kategori_c == 'Oli Motor' : real_kategori = 1324
            elif kategori_c == 'Octane Booster' : real_kategori = 1325
            elif kategori_c == 'Penghemat BBM' : real_kategori = 1326
            elif kategori_c == 'Oli & Penghemat BBM Lainnya' : real_kategori = 1328
            elif kategori_c == 'Busi' : real_kategori = 1334
            elif kategori_c == 'Kampas Rem' : real_kategori = 1335
            elif kategori_c == 'Kopling' : real_kategori = 1336
            elif kategori_c == 'Filter Udara' : real_kategori = 1337
            elif kategori_c == 'Radiator & Komponen' : real_kategori = 1378
            elif kategori_c == 'Shockbreaker' : real_kategori = 1379
            elif kategori_c == 'Bearing' : real_kategori = 1338
            elif kategori_c == 'Gearbox' : real_kategori = 1339
            elif kategori_c == 'Belt' : real_kategori = 1340
            elif kategori_c == 'Piston' : real_kategori = 1341
            elif kategori_c == 'Spare Part Mobil Lainnya' : real_kategori = 1342
            elif kategori_c == 'Busi' : real_kategori = 1343
            elif kategori_c == 'Kampas Rem' : real_kategori = 1344
            elif kategori_c == 'Kaliper, Cakram dan Tromol' : real_kategori = 1377
            elif kategori_c == 'Kabel  Selang' : real_kategori = 1359
            elif kategori_c == 'Aki Motor' : real_kategori = 1360
            elif kategori_c == 'CDI - ECU' : real_kategori = 1361
            elif kategori_c == 'Kopling' : real_kategori = 1345
            elif kategori_c == 'Bearing' : real_kategori = 1346
            elif kategori_c == 'Rantai & Gir' : real_kategori = 1347
            elif kategori_c == 'Filter Udara' : real_kategori = 1348
            elif kategori_c == 'V-Belt' : real_kategori = 1349
            elif kategori_c == 'Piston' : real_kategori = 1350
            elif kategori_c == 'Noken As' : real_kategori = 1362
            elif kategori_c == 'Koil' : real_kategori = 1355
            elif kategori_c == 'Karburator' : real_kategori = 1351
            elif kategori_c == 'Spare Part Motor Lainnya' : real_kategori = 1352
            elif kategori_c == 'Bola' : real_kategori = 1382
            elif kategori_c == 'Jersey Bola' : real_kategori = 1383
            elif kategori_c == 'Jaket Bola' : real_kategori = 1384
            elif kategori_c == 'Sepatu Bola' : real_kategori = 1385
            elif kategori_c == 'Sepatu Futsal' : real_kategori = 1483
            elif kategori_c == 'Kaos Kaki' : real_kategori = 1386
            elif kategori_c == 'Sepak Bola & Futsal Lainnya' : real_kategori = 1387
            elif kategori_c == 'Bola Basket' : real_kategori = 1389
            elif kategori_c == 'Ring Basket' : real_kategori = 1390
            elif kategori_c == 'Baju Basket' : real_kategori = 1391
            elif kategori_c == 'Sepatu Basket' : real_kategori = 1392
            elif kategori_c == 'Basket Lainnya' : real_kategori = 1393
            elif kategori_c == 'Raket Badminton' : real_kategori = 1395
            elif kategori_c == 'Shuttlecock' : real_kategori = 1396
            elif kategori_c == 'Sepatu Badminton' : real_kategori = 1397
            elif kategori_c == 'Badminton Lainnya' : real_kategori = 1398
            elif kategori_c == 'Sepeda' : real_kategori = 1405
            elif kategori_c == 'Frame Sepeda' : real_kategori = 1406
            elif kategori_c == 'Lampu Sepeda' : real_kategori = 1507
            elif kategori_c == 'Spare Part & Aksesoris Sepeda' : real_kategori = 1508
            elif kategori_c == 'Jersey & Celana Sepeda' : real_kategori = 1509
            elif kategori_c == 'Helm Sepeda' : real_kategori = 1510
            elif kategori_c == 'Sarung Tangan Sepeda' : real_kategori = 1511
            elif kategori_c == 'Sepeda Lainnya' : real_kategori = 1512
            elif kategori_c == 'Alat Fitness' : real_kategori = 1448
            elif kategori_c == 'Baju Olahraga Pria' : real_kategori = 1513
            elif kategori_c == 'Celana Olahraga Pria' : real_kategori = 1514
            elif kategori_c == 'Setelan Olahraga Pria' : real_kategori = 1449
            elif kategori_c == 'Baju Olahraga Wanita' : real_kategori = 1515
            elif kategori_c == 'Celana Olahraga Wanita' : real_kategori = 1516
            elif kategori_c == 'Setelan Olahraga Wanita' : real_kategori = 1505
            elif kategori_c == 'Sepatu Olahraga' : real_kategori = 1450
            elif kategori_c == 'Gym & Fitness Lainnya' : real_kategori = 1451
            elif kategori_c == 'Celana Renang Pria' : real_kategori = 1422
            elif kategori_c == 'Baju Renang Wanita' : real_kategori = 1423
            elif kategori_c == 'Baju Renang Anak Cowok' : real_kategori = 1424
            elif kategori_c == 'Baju Renang Anak Cewek' : real_kategori = 1425
            elif kategori_c == 'Kacamata Renang' : real_kategori = 1426
            elif kategori_c == 'Topi Renang' : real_kategori = 1427
            elif kategori_c == 'Pelampung' : real_kategori = 1429
            elif kategori_c == 'Kolam Karet' : real_kategori = 1430
            elif kategori_c == 'Alat Snorkeling' : real_kategori = 1428
            elif kategori_c == 'Wetsuit & Drysuit' : real_kategori = 1467
            elif kategori_c == 'Diving Fin' : real_kategori = 1468
            elif kategori_c == 'Diving Mask' : real_kategori = 1469
            elif kategori_c == 'Senter Diving' : real_kategori = 1470
            elif kategori_c == 'Alat Scuba' : real_kategori = 1471
            elif kategori_c == 'Aksesoris Diving' : real_kategori = 1472
            elif kategori_c == 'Renang & Diving Lainnya' : real_kategori = 1431
            elif kategori_c == 'Jaket Gunung' : real_kategori = 1484
            elif kategori_c == 'Celana Gunung' : real_kategori = 1485
            elif kategori_c == 'Setelan Pakaian Gunung' : real_kategori = 1486
            elif kategori_c == 'Sepatu Gunung' : real_kategori = 1487
            elif kategori_c == 'Tas Gunung' : real_kategori = 216
            elif kategori_c == 'Lampu Camping' : real_kategori = 1488
            elif kategori_c == 'Senter Camping' : real_kategori = 1489
            elif kategori_c == 'Headlamp' : real_kategori = 1490
            elif kategori_c == 'Teropong' : real_kategori = 1434
            elif kategori_c == 'Kompas' : real_kategori = 1435
            elif kategori_c == 'Walkie-talkie' : real_kategori = 1436
            elif kategori_c == 'Carabiner' : real_kategori = 1491
            elif kategori_c == 'Trekking Pole' : real_kategori = 1492
            elif kategori_c == 'Survival Kit' : real_kategori = 1493
            elif kategori_c == 'Tenda' : real_kategori = 1433
            elif kategori_c == 'Sleeping Bag' : real_kategori = 1494
            elif kategori_c == 'Alat Masak Camping' : real_kategori = 1495
            elif kategori_c == 'Perahu Karet' : real_kategori = 1496
            elif kategori_c == 'Outdoor Sport Lainnya' : real_kategori = 1438
            elif kategori_c == 'Joran Pancing' : real_kategori = 1453
            elif kategori_c == 'Fishing Reel' : real_kategori = 1454
            elif kategori_c == 'Senar Pancing' : real_kategori = 1455
            elif kategori_c == 'Kail Pancing' : real_kategori = 1456
            elif kategori_c == 'Umpan Pancing' : real_kategori = 1457
            elif kategori_c == 'Fish Finder' : real_kategori = 1458
            elif kategori_c == 'Set Alat Pancing' : real_kategori = 1473
            elif kategori_c == 'Tas Pancing' : real_kategori = 1474
            elif kategori_c == 'Alat Pancing Lainnya' : real_kategori = 1459
            elif kategori_c == 'Knuckle' : real_kategori = 1497
            elif kategori_c == 'Baton' : real_kategori = 1500
            elif kategori_c == 'Nunchaku' : real_kategori = 1501
            elif kategori_c == 'Beladiri Lainnya' : real_kategori = 1504
            elif kategori_c == 'Baterai & Gas Airsoft' : real_kategori = 1439
            elif kategori_c == 'Scope' : real_kategori = 1440
            elif kategori_c == 'Holster, Case & Tas' : real_kategori = 1441
            elif kategori_c == 'Baju & Rompi Airsoft' : real_kategori = 1442
            elif kategori_c == 'Pad & Glove Airsoft' : real_kategori = 1443
            elif kategori_c == 'Helm & Topi Airsoft' : real_kategori = 1444
            elif kategori_c == 'Topeng & Balaclava' : real_kategori = 1445
            elif kategori_c == 'Goggle & Kacamata' : real_kategori = 1446
            elif kategori_c == 'Sepatu Airsoft' : real_kategori = 1447
            elif kategori_c == 'Airsoft Gun Lainnya' : real_kategori = 496
            elif kategori_c == 'Raket Tenis' : real_kategori = 1400
            elif kategori_c == 'Bola Tenis' : real_kategori = 1401
            elif kategori_c == 'Sepatu Tenis' : real_kategori = 1402
            elif kategori_c == 'Tenis Lainnya' : real_kategori = 1403
            elif kategori_c == 'Headband' : real_kategori = 1461
            elif kategori_c == 'Wristband' : real_kategori = 1462
            elif kategori_c == 'Bracer' : real_kategori = 1506
            elif kategori_c == 'Stopwatch' : real_kategori = 1464
            elif kategori_c == 'Tas Olahraga' : real_kategori = 1463
            elif kategori_c == 'Aksesoris Olahraga Lainnya' : real_kategori = 1466
            elif kategori_c == 'Busur' : real_kategori = 1479
            elif kategori_c == 'Panah' : real_kategori = 1480
            elif kategori_c == 'Akesoris Panahan' : real_kategori = 1481
            elif kategori_c == 'Panahan Lainnya' : real_kategori = 1482
            elif kategori_b == 'Olahraga Lainnya' : real_kategori = 1465
            elif kategori_b == 'Movie & Serial TV' : real_kategori = 17
            elif kategori_c == 'CD & DVD Musik' : real_kategori = 1517
            elif kategori_c == 'Alat Musik' : real_kategori = 1518
            elif kategori_c == 'Musik Lainnya' : real_kategori = 1519
            elif kategori_c == 'Blender & Juicer' : real_kategori = 921
            elif kategori_c == 'Mixer' : real_kategori = 922
            elif kategori_c == 'Dispenser Minuman' : real_kategori = 916
            elif kategori_c == 'Pompa Galon' : real_kategori = 1191
            elif kategori_c == 'Water Purelifier' : real_kategori = 917
            elif kategori_c == 'Kulkas & Cooler Box' : real_kategori = 918
            elif kategori_c == 'Timbangan Dapur' : real_kategori = 958
            elif kategori_c == 'Gelas & Sendok Takar' : real_kategori = 957
            elif kategori_c == 'Pembuka Botol & Kaleng' : real_kategori = 931
            elif kategori_c == 'Cetakan Es, Puding, Coklat' : real_kategori = 961
            elif kategori_c == 'Celemek' : real_kategori = 933
            elif kategori_c == 'Pelindung Tangan' : real_kategori = 934
            elif kategori_c == 'Saringan' : real_kategori = 1193
            elif kategori_c == 'Sarung Galon & Kulkas' : real_kategori = 935
            elif kategori_c == 'Magnet Kulkas' : real_kategori = 936
            elif kategori_c == 'Perlengkapan Cuci Piring' : real_kategori = 939
            elif kategori_c == 'Peralatan Dapur Lainnya' : real_kategori = 919
            elif kategori_c == 'Kompor' : real_kategori = 912
            elif kategori_c == 'Regulator & Penghemat Gas' : real_kategori = 913
            elif kategori_c == 'Korek Kompor' : real_kategori = 1190
            elif kategori_c == 'Oven' : real_kategori = 914
            elif kategori_c == 'Microwave' : real_kategori = 915
            elif kategori_c == 'Rice Cooker' : real_kategori = 920
            elif kategori_c == 'Panci' : real_kategori = 948
            elif kategori_c == 'Wajan' : real_kategori = 949
            elif kategori_c == 'Presto' : real_kategori = 946
            elif kategori_c == 'Griller' : real_kategori = 951
            elif kategori_c == 'Steamer' : real_kategori = 950
            elif kategori_c == 'Teko & Pemanas Air' : real_kategori = 952
            elif kategori_c == 'Spatula & Sutil' : real_kategori = 953
            elif kategori_c == 'Capit Makanan' : real_kategori = 1194
            elif kategori_c == 'Peralatan Masak Lainnya' : real_kategori = 954
            elif kategori_c == 'Pisau Dapur' : real_kategori = 963
            elif kategori_c == 'Pengasah Pisau' : real_kategori = 964
            elif kategori_c == 'Talenan' : real_kategori = 965
            elif kategori_c == 'Gunting Dapur' : real_kategori = 1532
            elif kategori_c == 'Parutan' : real_kategori = 955
            elif kategori_c == 'Peeler' : real_kategori = 1195
            elif kategori_c == 'Chopper' : real_kategori = 1533
            elif kategori_c == 'Grinder' : real_kategori = 923
            elif kategori_c == 'Pisau Lainnya' : real_kategori = 967
            elif kategori_c == 'Coffee & Tea Maker' : real_kategori = 1197
            elif kategori_c == 'Ice & Yogurt Maker' : real_kategori = 1198
            elif kategori_c == 'Toaster' : real_kategori = 1199
            elif kategori_c == 'Waffle & Pancake Maker' : real_kategori = 1200
            elif kategori_c == 'Donut Maker' : real_kategori = 1201
            elif kategori_c == 'Biscuit & Cookie Maker' : real_kategori = 1202
            elif kategori_c == 'Snack Maker' : real_kategori = 1203
            elif kategori_c == 'Cake Maker' : real_kategori = 1204
            elif kategori_c == 'Alat Penghias Kue' : real_kategori = 1205
            elif kategori_c == 'Chocolate Melter' : real_kategori = 1206
            elif kategori_c == 'Noodle & Pasta Maker' : real_kategori = 1207
            elif kategori_c == 'Sushi Roller' : real_kategori = 1208
            elif kategori_c == 'Food & Drink Maker Lainnya' : real_kategori = 1209
            elif kategori_c == 'Sendok & Garpu' : real_kategori = 968
            elif kategori_c == 'Sumpit' : real_kategori = 969
            elif kategori_c == 'Centong Nasi & Sendok Sayur' : real_kategori = 1210
            elif kategori_c == 'Piring Makan' : real_kategori = 970
            elif kategori_c == 'Mangkok Makan' : real_kategori = 971
            elif kategori_c == 'Piring & Mangkok Saji' : real_kategori = 1211
            elif kategori_c == 'Gelas & Mug' : real_kategori = 972
            elif kategori_c == 'Pitcher' : real_kategori = 1212
            elif kategori_c == 'Paket Peralatan Makan' : real_kategori = 973
            elif kategori_c == 'Paket Peralatan Minum' : real_kategori = 974
            elif kategori_c == 'Tutup Gelas & Piring' : real_kategori = 976
            elif kategori_c == 'Tatakan Gelas & Piring' : real_kategori = 977
            elif kategori_c == 'Tempat Sendok & Garpu' : real_kategori = 940
            elif kategori_c == 'Rak Piring & Tempat Gelas' : real_kategori = 1213
            elif kategori_c == 'Tudung Saji' : real_kategori = 975
            elif kategori_c == 'Nampan' : real_kategori = 979
            elif kategori_c == 'Peralatan Makan Lainnya' : real_kategori = 982
            elif kategori_c == 'Kotak Makan & Rantang' : real_kategori = 980
            elif kategori_c == 'Botol Minum & Termos' : real_kategori = 981
            elif kategori_c == 'Tas Bekal' : real_kategori = 1216
            elif kategori_c == 'Tas Botol' : real_kategori = 1217
            elif kategori_c == 'Cetakan Bento' : real_kategori = 1218
            elif kategori_c == 'Cup Bento' : real_kategori = 1219
            elif kategori_c == 'Partisi Bento' : real_kategori = 1220
            elif kategori_c == 'Tusuk Bento' : real_kategori = 1221
            elif kategori_c == 'Bekal Lainnya' : real_kategori = 1222
            elif kategori_c == 'Toples' : real_kategori = 1036
            elif kategori_c == 'Tempat Bumbu' : real_kategori = 932
            elif kategori_c == 'Tempat Saos & Kecap' : real_kategori = 1224
            elif kategori_c == 'Tempat Roti' : real_kategori = 1225
            elif kategori_c == 'Tempat Buah & Sayur' : real_kategori = 1226
            elif kategori_c == 'Sealer' : real_kategori = 1534
            elif kategori_c == 'Plastic Wrap' : real_kategori = 1535
            elif kategori_c == 'Penyimpanan Makanan Lainnya' : real_kategori = 1227
            elif kategori_b == 'Dapur Lainnya' : real_kategori = 1130
            elif kategori_c == 'Pensil' : real_kategori = 643
            elif kategori_c == 'Pulpen' : real_kategori = 1077
            elif kategori_c == 'Penghapus' : real_kategori = 644
            elif kategori_c == 'Correction (Tip-X)' : real_kategori = 1078
            elif kategori_c == 'Highlighter' : real_kategori = 1079
            elif kategori_c == 'Rautan' : real_kategori = 1080
            elif kategori_c == 'Penggaris' : real_kategori = 1081
            elif kategori_c == 'Tempat Pensil' : real_kategori = 645
            elif kategori_c == 'Paket Alat Tulis' : real_kategori = 1082
            elif kategori_c == 'Stationery Stand' : real_kategori = 1238
            elif kategori_c == 'Spidol Papan Tulis' : real_kategori = 1083
            elif kategori_c == 'Papan Tulis & Tempel' : real_kategori = 1084
            elif kategori_c == 'Alat Tulis Lainnya' : real_kategori = 1085
            elif kategori_c == 'Pensil Warna' : real_kategori = 646
            elif kategori_c == 'Spidol Warna' : real_kategori = 1087
            elif kategori_c == 'Crayon' : real_kategori = 1088
            elif kategori_c == 'Oil & Dry Pastel' : real_kategori = 1089
            elif kategori_c == 'Cat Air' : real_kategori = 1090
            elif kategori_c == 'Cat Minyak' : real_kategori = 1091
            elif kategori_c == 'Cat Poster' : real_kategori = 1239
            elif kategori_c == 'Cat Akrilik' : real_kategori = 1240
            elif kategori_c == 'Art Set' : real_kategori = 1241
            elif kategori_c == 'Kuas Lukis' : real_kategori = 1092
            elif kategori_c == 'Palet' : real_kategori = 1093
            elif kategori_c == 'Buku Gambar & Sketsa' : real_kategori = 1094
            elif kategori_c == 'Kanvas Lukis' : real_kategori = 1095
            elif kategori_c == 'Alat Kesenian Lainnya' : real_kategori = 1096
            elif kategori_c == 'Kertas Print & Fotocopy' : real_kategori = 1100
            elif kategori_c == 'Kertas Fax' : real_kategori = 1242
            elif kategori_c == 'Kertas File' : real_kategori = 1101
            elif kategori_c == 'Memo & Sticky Notes' : real_kategori = 1103
            elif kategori_c == 'Buku Catatan' : real_kategori = 648
            elif kategori_c == 'Buku Tulis' : real_kategori = 1258
            elif kategori_c == 'Buku Keuangan' : real_kategori = 1243
            elif kategori_c == 'Buku Telepon & Alamat' : real_kategori = 1104
            elif kategori_c == 'Pembatas Buku' : real_kategori = 1124
            elif kategori_c == 'Sampul Buku' : real_kategori = 1244
            elif kategori_c == 'Pembolong Kertas' : real_kategori = 1245
            elif kategori_c == 'Penghancur Kertas' : real_kategori = 1246
            elif kategori_c == 'Kertas Lainnya' : real_kategori = 1105
            elif kategori_c == 'Amplop' : real_kategori = 647
            elif kategori_c == 'Kertas Surat' : real_kategori = 1102
            elif kategori_c == 'Kartu Pos' : real_kategori = 1126
            elif kategori_c == 'Perangko' : real_kategori = 1125
            elif kategori_c == 'Stempel' : real_kategori = 1127
            elif kategori_c == 'Surat-Menyurat Lainnya' : real_kategori = 1249
            elif kategori_c == 'Staples' : real_kategori = 1109
            elif kategori_c == 'Klip Kertas' : real_kategori = 1110
            elif kategori_c == 'Klip Kabel' : real_kategori = 1250
            elif kategori_c == 'Lem Kertas' : real_kategori = 1107
            elif kategori_c == 'Selotip & Double Tape' : real_kategori = 1108
            elif kategori_c == 'Stiker' : real_kategori = 653
            elif kategori_c == 'Pengikat & Perekat Lainnya' : real_kategori = 1111
            elif kategori_c == 'Gunting' : real_kategori = 1123
            elif kategori_c == 'Cutter' : real_kategori = 1252
            elif kategori_c == 'Art Knelife' : real_kategori = 1253
            elif kategori_c == 'Cutting Mat' : real_kategori = 1254
            elif kategori_c == 'Alat Pemotong Kertas Lainnya' : real_kategori = 1255
            elif kategori_c == 'Binder' : real_kategori = 1113
            elif kategori_c == 'Map' : real_kategori = 650
            elif kategori_c == 'Card Holder' : real_kategori = 1114
            elif kategori_c == 'Box File' : real_kategori = 1256
            elif kategori_c == 'Passport Cover' : real_kategori = 1257
            elif kategori_c == 'Document & Desk Organizer Lainnya' : real_kategori = 1115
            elif kategori_c == 'Kalkulator' : real_kategori = 652
            elif kategori_c == 'Kamus Elektronik' : real_kategori = 1117
            elif kategori_b == 'Office & Stationery Lainnya' : real_kategori = 1122
            elif kategori_c == 'Boneka Beruang' : real_kategori = 2349
            elif kategori_c == 'Boneka Binatang' : real_kategori = 2353
            elif kategori_c == 'Boneka Edukasi' : real_kategori = 2351
            elif kategori_c == 'Boneka Wisuda' : real_kategori = 2350
            elif kategori_c == 'Boneka Barbie' : real_kategori = 2405
            elif kategori_c == 'Boneka Karakter' : real_kategori = 2354
            elif kategori_c == 'Boneka Bantal' : real_kategori = 2355
            elif kategori_c == 'Boneka Lainnya' : real_kategori = 2404
            elif kategori_c == 'Plastik' : real_kategori = 2395
            elif kategori_c == 'Kotak dan Kertas Kado' : real_kategori = 2392
            elif kategori_c == 'Pita Kado' : real_kategori = 2397
            elif kategori_c == 'Bungkus dan Kemasan Lainnya' : real_kategori = 2398
            elif kategori_c == 'Bubble Wrap' : real_kategori = 2396
            elif kategori_c == 'Tas Kertas' : real_kategori = 2393
            elif kategori_c == 'Kardus' : real_kategori = 2394
            elif kategori_c == 'Uang Kuno' : real_kategori = 2367
            elif kategori_c == 'Hadiah Custom' : real_kategori = 2365
            elif kategori_c == 'Gantungan Kunci' : real_kategori = 2361
            elif kategori_c == 'Miniatur dan Karikatur' : real_kategori = 2364
            elif kategori_c == 'Kartu Ucapan' : real_kategori = 2369
            elif kategori_c == 'Trophy dan Medali' : real_kategori = 2363
            elif kategori_c == 'Korek Api' : real_kategori = 2368
            elif kategori_c == 'Magnet Kulkas' : real_kategori = 2366
            elif kategori_c == 'Celengan' : real_kategori = 2362
            elif kategori_c == 'Hadiah Lainnya' : real_kategori = 2370
            elif kategori_b == 'Kerajinan Tangan' : real_kategori = 10
            elif kategori_c == 'Bunga Lainnya' : real_kategori = 2402
            elif kategori_c == 'Bunga Papan' : real_kategori = 2401
            elif kategori_c == 'Buket Bunga' : real_kategori = 2400
            elif kategori_c == 'Balon Karet dan Latex' : real_kategori = 2356
            elif kategori_c == 'Balon Lainnya' : real_kategori = 2381
            elif kategori_c == 'Balon Karakter' : real_kategori = 2357
            elif kategori_c == 'Balon Huruf dan Angka' : real_kategori = 2358
            elif kategori_c == 'Voucher' : real_kategori = 2388
            elif kategori_c == 'Souvenir Pernikahan' : real_kategori = 2384
            elif kategori_c == 'Hampers' : real_kategori = 2386
            elif kategori_c == 'Souvenir Ulang Tahun' : real_kategori = 2385
            elif kategori_c == 'Souvenir Lainnya' : real_kategori = 2390
            elif kategori_c == 'Perlengkapan Pesta Lainnya' : real_kategori = 2380
            elif kategori_c == 'Lampion' : real_kategori = 2373
            elif kategori_c == 'Lilin' : real_kategori = 2374
            elif kategori_c == 'Undangan' : real_kategori = 2379
            elif kategori_c == 'Backdrop' : real_kategori = 2378
            elif kategori_c == 'Piring dan Gelas Kertas' : real_kategori = 2377
            elif kategori_c == 'Pompom' : real_kategori = 2372
            elif kategori_c == 'Banner' : real_kategori = 2371
            elif kategori_c == 'Mahar dan Seserahan' : real_kategori = 2376
            elif kategori_c == 'Topeng' : real_kategori = 2375
            elif kategori_b == 'Lainnya' : real_kategori = 11
            elif kategori_c == 'Action Figure' : real_kategori = 471
            elif kategori_c == 'Super Deformed Figure' : real_kategori = 473
            elif kategori_c == 'Figure Set' : real_kategori = 472
            elif kategori_c == 'Figure Lainnya' : real_kategori = 475
            elif kategori_c == 'Mecha Model (Gunpla)' : real_kategori = 476
            elif kategori_c == 'Vehicle Model (Tamiya)' : real_kategori = 506
            elif kategori_c == 'Brick (Lego)' : real_kategori = 477
            elif kategori_c == 'Part Mini 4WD (Tamiya)' : real_kategori = 511
            elif kategori_c == 'Tool & Kit Mecha Model (Gunpla)' : real_kategori = 507
            elif kategori_c == 'Model Kit Lainnya' : real_kategori = 478
            elif kategori_c == 'Diecast Mobil' : real_kategori = 479
            elif kategori_c == 'Diecast Bus' : real_kategori = 508
            elif kategori_c == 'Diecast Truk & Konstruksi' : real_kategori = 480
            elif kategori_c == 'Diecast Kendaraan Publik' : real_kategori = 481
            elif kategori_c == 'Diecast Militer' : real_kategori = 482
            elif kategori_c == 'Diecast Motor & Sepeda' : real_kategori = 483
            elif kategori_c == 'Diecast Pesawat' : real_kategori = 484
            elif kategori_c == 'Diecast Kapal' : real_kategori = 509
            elif kategori_c == 'Bangunan & Track Diecast' : real_kategori = 510
            elif kategori_c == 'Diecast Set' : real_kategori = 474
            elif kategori_c == 'Diecast Lainnya' : real_kategori = 485
            elif kategori_c == 'Helikopter RC' : real_kategori = 514
            elif kategori_c == 'Pesawat RC' : real_kategori = 515
            elif kategori_c == 'Mobil & Truk RC' : real_kategori = 516
            elif kategori_c == 'Kapal RC' : real_kategori = 517
            elif kategori_c == 'Part RC' : real_kategori = 518
            elif kategori_c == 'Mainan Remote Control Lainnya' : real_kategori = 519
            elif kategori_b == 'Mainan Anak' : real_kategori = 500
            elif kategori_c == 'Kartu' : real_kategori = 497
            elif kategori_c == 'Puzzle' : real_kategori = 498
            elif kategori_c == 'Board Game' : real_kategori = 499
            elif kategori_c == 'Sulap' : real_kategori = 501
            elif kategori_c == 'Gag & Prank Toy' : real_kategori = 544
            elif kategori_c == 'Miniatur' : real_kategori = 504
            elif kategori_c == 'Alat Berkebun & Hewan Peliharaan' : real_kategori = 520
            elif kategori_c == 'Peralatan Camping & Olahraga Outdoor' : real_kategori = 545
            elif kategori_c == 'Lainnya Lainnya' : real_kategori = 505
            elif kategori_c == 'Biskuit Krakers' : real_kategori = 1135
            elif kategori_c == 'Kue' : real_kategori = 1136
            elif kategori_c == 'Kue Kering' : real_kategori = 1137
            elif kategori_c == 'Wafer' : real_kategori = 1138
            elif kategori_c == 'Rolls' : real_kategori = 1139
            elif kategori_c == 'Biskuit & Kue Lainnya' : real_kategori = 1140
            elif kategori_c == 'Buah' : real_kategori = 2307
            elif kategori_c == 'Daging' : real_kategori = 2303
            elif kategori_c == 'Daging Olahan' : real_kategori = 2304
            elif kategori_c == 'Dessert' : real_kategori = 2305
            elif kategori_c == 'Permen' : real_kategori = 1142
            elif kategori_c == 'Cokelat' : real_kategori = 1146
            elif kategori_c == 'Buah-buahan' : real_kategori = 1147
            elif kategori_c == 'Selai' : real_kategori = 1148
            elif kategori_c == 'Makanan Manis Lainnya' : real_kategori = 1149
            elif kategori_c == 'Daging Kering & Asin' : real_kategori = 1151
            elif kategori_c == 'Mie & Pasta' : real_kategori = 1152
            elif kategori_c == 'Olahan Kacang' : real_kategori = 1153
            elif kategori_c == 'Keripik' : real_kategori = 1154
            elif kategori_c == 'Makanan Ringan' : real_kategori = 1155
            elif kategori_c == 'Sereal' : real_kategori = 1156
            elif kategori_c == 'Camilan Tradisional' : real_kategori = 1157
            elif kategori_c == 'Makanan Kering Lainnya' : real_kategori = 1158
            elif kategori_c == 'Teh' : real_kategori = 1174
            elif kategori_c == 'Kopi' : real_kategori = 1175
            elif kategori_c == 'Krimer & Gula' : real_kategori = 1176
            elif kategori_c == 'Susu' : real_kategori = 1177
            elif kategori_c == 'Minuman Rasa' : real_kategori = 1178
            elif kategori_c == 'Minuman Kaleng  Cup' : real_kategori = 1179
            elif kategori_c == 'Minuman Lainnya' : real_kategori = 1180
            elif kategori_c == 'Susu Nutrisi' : real_kategori = 1182
            elif kategori_c == 'Madu' : real_kategori = 1183
            elif kategori_c == 'Makanan Diet' : real_kategori = 1184
            elif kategori_c == 'Minuman Kesehatan' : real_kategori = 1185
            elif kategori_c == 'Makanan & Minuman Kesehatan Lainnya' : real_kategori = 1186
            elif kategori_c == 'Seafood Kering' : real_kategori = 1168
            elif kategori_c == 'Modern Snack' : real_kategori = 1169
            elif kategori_c == 'Daging Olahan' : real_kategori = 1170
            elif kategori_c == 'Makanan Siap Saji Lainnya' : real_kategori = 1172
            elif kategori_c == 'Minyak' : real_kategori = 1160
            elif kategori_c == 'Salt & Spices' : real_kategori = 1161
            elif kategori_c == 'Saus & Bumbu' : real_kategori = 1162
            elif kategori_c == 'Tepung' : real_kategori = 1163
            elif kategori_c == 'Kaldu' : real_kategori = 1164
            elif kategori_c == 'Sambal' : real_kategori = 1165
            elif kategori_c == 'Bumbu & Bahan Dasar Lainnya' : real_kategori = 1166
            elif kategori_b == 'Makanan & Minuman Lainnya' : real_kategori = 1187
            elif kategori_c == 'Kisah Nyata' : real_kategori = 754
            elif kategori_c == 'Fantasi' : real_kategori = 749
            elif kategori_c == 'Misteri' : real_kategori = 748
            elif kategori_c == 'Novel Indonesia' : real_kategori = 752
            elif kategori_c == 'Novel Remaja' : real_kategori = 751
            elif kategori_c == 'Novel Terjemahan' : real_kategori = 753
            elif kategori_c == 'Puisi' : real_kategori = 755
            elif kategori_c == 'Roman' : real_kategori = 747
            elif kategori_c == 'Science Fiction' : real_kategori = 750
            elif kategori_c == 'Cerita Anak' : real_kategori = 758
            elif kategori_c == 'Keterampilan Anak' : real_kategori = 759
            elif kategori_c == 'Dunia Pengetahuan' : real_kategori = 760
            elif kategori_c == 'Komik' : real_kategori = 757
            elif kategori_c == 'Biografi' : real_kategori = 762
            elif kategori_c == 'Komunikasi' : real_kategori = 765
            elif kategori_c == 'Lingkungan Hidup' : real_kategori = 764
            elif kategori_c == 'Politik' : real_kategori = 763
            elif kategori_c == 'Sejarah' : real_kategori = 1132
            elif kategori_c == 'Sosial Budaya' : real_kategori = 766
            elif kategori_c == 'Alam' : real_kategori = 772
            elif kategori_c == 'Fotografi' : real_kategori = 776
            elif kategori_c == 'Hewan Peliharaan' : real_kategori = 778
            elif kategori_c == 'Hiburan' : real_kategori = 769
            elif kategori_c == 'Humor' : real_kategori = 777
            elif kategori_c == 'Keterampilan' : real_kategori = 780
            elif kategori_c == 'Kuliner' : real_kategori = 768
            elif kategori_c == 'Musik & Lagu' : real_kategori = 771
            elif kategori_c == 'Olahraga' : real_kategori = 774
            elif kategori_c == 'Permainan' : real_kategori = 779
            elif kategori_c == 'Seni' : real_kategori = 775
            elif kategori_c == 'Tanaman' : real_kategori = 781
            elif kategori_c == 'Travel' : real_kategori = 770
            elif kategori_b == 'Majalah' : real_kategori = 782
            elif kategori_c == 'Bangunan' : real_kategori = 784
            elif kategori_c == 'Codes & Standars' : real_kategori = 788
            elif kategori_c == 'Dekorasi & Ornamen' : real_kategori = 785
            elif kategori_c == 'Desain Dapur' : real_kategori = 792
            elif kategori_c == 'Desain Kamar' : real_kategori = 790
            elif kategori_c == 'Desain Ruang  Keluarga' : real_kategori = 793
            elif kategori_c == 'Desain Ruang Tamu' : real_kategori = 791
            elif kategori_c == 'Desain Rumah' : real_kategori = 789
            elif kategori_c == 'Taman' : real_kategori = 787
            elif kategori_c == 'Interior & Eksterior' : real_kategori = 786
            elif kategori_c == 'Metode & Material Bangunan' : real_kategori = 794
            elif kategori_c == 'Astronomi' : real_kategori = 805
            elif kategori_c == 'Bahasa' : real_kategori = 810
            elif kategori_c == 'Biologi' : real_kategori = 804
            elif kategori_c == 'Ekonomi' : real_kategori = 796
            elif kategori_c == 'Elektro & Elektronik' : real_kategori = 822
            elif kategori_c == 'Ensiklopedia' : real_kategori = 821
            elif kategori_c == 'Fisika' : real_kategori = 800
            elif kategori_c == 'Geografi' : real_kategori = 808
            elif kategori_c == 'Geologi' : real_kategori = 809
            elif kategori_c == 'Hukum' : real_kategori = 802
            elif kategori_c == 'Ilmiah' : real_kategori = 820
            elif kategori_c == 'Kesekretariatan' : real_kategori = 811
            elif kategori_c == 'Kimia' : real_kategori = 801
            elif kategori_c == 'Manajemen' : real_kategori = 797
            elif kategori_c == 'Matematika' : real_kategori = 799
            elif kategori_c == 'Mesin' : real_kategori = 823
            elif kategori_c == 'Pariwisata' : real_kategori = 813
            elif kategori_c == 'Pengetahuan Umum' : real_kategori = 1133
            elif kategori_c == 'Perhotelan' : real_kategori = 812
            elif kategori_c == 'Perikanan' : real_kategori = 816
            elif kategori_c == 'Perkebunan' : real_kategori = 817
            elif kategori_c == 'Perpajakan' : real_kategori = 798
            elif kategori_c == 'Pertanian' : real_kategori = 815
            elif kategori_c == 'Peta & Bola Dunia' : real_kategori = 814
            elif kategori_c == 'Peternakan' : real_kategori = 818
            elif kategori_c == 'Psikologi' : real_kategori = 803
            elif kategori_c == 'Sipil' : real_kategori = 824
            elif kategori_c == 'Statistik' : real_kategori = 806
            elif kategori_c == 'Teknik' : real_kategori = 807
            elif kategori_c == 'Buddha' : real_kategori = 828
            elif kategori_c == 'Filosofi' : real_kategori = 834
            elif kategori_c == 'Filsafat' : real_kategori = 831
            elif kategori_c == 'Hindu' : real_kategori = 829
            elif kategori_c == 'Islam' : real_kategori = 826
            elif kategori_c == 'Kepercayaan' : real_kategori = 832
            elif kategori_c == 'Khong Hu Chu' : real_kategori = 830
            elif kategori_c == 'Kristen & Katolik' : real_kategori = 827
            elif kategori_c == 'Spiritual' : real_kategori = 833
            elif kategori_c == 'Database' : real_kategori = 836
            elif kategori_c == 'Design Graphics' : real_kategori = 840
            elif kategori_c == 'Hardware' : real_kategori = 839
            elif kategori_c == 'Internet & Web' : real_kategori = 841
            elif kategori_c == 'Microsoft Office' : real_kategori = 838
            elif kategori_c == 'Mobile & Gadget' : real_kategori = 842
            elif kategori_c == 'Programming' : real_kategori = 837
            elif kategori_c == 'Sistem Operasi' : real_kategori = 843
            elif kategori_c == 'Social Media' : real_kategori = 844
            elif kategori_c == 'Farmasi' : real_kategori = 846
            elif kategori_c == 'Kedokteran Spesialis' : real_kategori = 848
            elif kategori_c == 'Kedokteran Umum' : real_kategori = 847
            elif kategori_c == 'Kesehatan' : real_kategori = 849
            elif kategori_c == 'Psikiatri' : real_kategori = 850
            elif kategori_c == 'Busana' : real_kategori = 854
            elif kategori_c == 'Kecantikan' : real_kategori = 857
            elif kategori_c == 'Kehamilan & Menyusui' : real_kategori = 852
            elif kategori_c == 'Nama-nama Bayi' : real_kategori = 853
            elif kategori_c == 'Bimbingan Orang Tua' : real_kategori = 858
            elif kategori_c == 'Pendidikan Keluarga' : real_kategori = 819
            elif kategori_c == 'Resep Makanan & Minuman' : real_kategori = 855
            elif kategori_c == 'Kesuksesan' : real_kategori = 861
            elif kategori_c == 'Leadership  Kepemimpinan' : real_kategori = 860
            elif kategori_c == 'Self Help' : real_kategori = 862
            elif kategori_c == 'Bimbingan Belajar' : real_kategori = 864
            elif kategori_c == 'Kumpulan Soal SD' : real_kategori = 865
            elif kategori_c == 'Kumpulan Soal SMP' : real_kategori = 866
            elif kategori_c == 'Kumpulan Soal SMA' : real_kategori = 867
            elif kategori_c == 'Buku SD Kelas 1' : real_kategori = 868
            elif kategori_c == 'Buku SD Kelas 2' : real_kategori = 869
            elif kategori_c == 'Buku SD Kelas 3' : real_kategori = 870
            elif kategori_c == 'Buku SD Kelas 4' : real_kategori = 871
            elif kategori_c == 'Buku SD Kelas 5' : real_kategori = 872
            elif kategori_c == 'Buku SD Kelas 6' : real_kategori = 873
            elif kategori_c == 'Buku SMP Kelas 1' : real_kategori = 874
            elif kategori_c == 'Buku SMP Kelas 2' : real_kategori = 875
            elif kategori_c == 'Buku SMP Kelas 3' : real_kategori = 876
            elif kategori_c == 'Buku SMA Kelas 1' : real_kategori = 877
            elif kategori_c == 'Buku SMA Kelas 2' : real_kategori = 878
            elif kategori_c == 'Buku SMA Kelas 3' : real_kategori = 879
            elif kategori_c == 'Agriculture' : real_kategori = 882
            elif kategori_c == 'Art & Novel' : real_kategori = 881
            elif kategori_c == 'Child & Teenager' : real_kategori = 887
            elif kategori_c == 'Computer' : real_kategori = 886
            elif kategori_c == 'Economy' : real_kategori = 884
            elif kategori_c == 'Femininity' : real_kategori = 885
            elif kategori_c == 'Health' : real_kategori = 883
            elif kategori_c == 'Hobby & Interest' : real_kategori = 888
            elif kategori_c == 'Language' : real_kategori = 889
            elif kategori_c == 'Law' : real_kategori = 890
            elif kategori_c == 'Management & Business' : real_kategori = 891
            elif kategori_c == 'Medical' : real_kategori = 892
            elif kategori_c == 'Political Social' : real_kategori = 893
            elif kategori_c == 'Psychology & Education' : real_kategori = 894
            elif kategori_c == 'Reference & Dictionary' : real_kategori = 895
            elif kategori_c == 'Religion & Philosophy' : real_kategori = 896
            elif kategori_c == 'School Book' : real_kategori = 897
            elif kategori_c == 'Secretarial' : real_kategori = 898
            elif kategori_c == 'Self Development & Career' : real_kategori = 899
            elif kategori_c == 'Technique' : real_kategori = 900
            elif kategori_c == 'Tourism & Map' : real_kategori = 901
            elif kategori_b == 'Buku Lainnya' : real_kategori = 902
            elif kategori_a == 'Software' : real_kategori = 20
            elif kategori_a == 'Produk Lainnya' : real_kategori = 36

            # urutan = nama produk, kategori, Deskripsi, Harga,	Berat,Pemesanan Minimum, Status, Jumlah Stok, Etalase, Preorder, Waktu Proses Preorder,	Kondisi, Gambar 1 	Gambar 2	Gambar 3	Gambar 4	Gambar 5
            
            insert = [nama, real_kategori]
                        
            sum = 0
            ignore_encode = []            

            print get_harga

            while (sum < len(description)) :
                try:
                    if (etree.tostring(description[sum]).find('<br/>') == 0):
                        ignore_encode.append('\n')
                except :
                    ignore_encode.append((description[sum].encode('ascii', 'ignore')))
                sum = sum + 1

            # print etree.tostring(description[1]).find('<br/>')
            new_desc = ''.join(ignore_encode)
            insert.append(new_desc[12:])

            buntut = [harga_margin(int(harga)), berat, minBeli, 'Stok Tersedia', '', kategori_a, '', '', kondisi]    
            final = insert + buntut

            start = 0
            while (start < len(image)):
                # namefile = 'gambar' ,str(sum), '.jpg'
                gambar = image[start].replace('100', '300')
                final.append(gambar)
                start = start + 1

            if not os.path.exists(pemilik_barang):
                os.makedirs(pemilik_barang)

            with open(pemilik_barang + '/another.csv', 'a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(final)
        
        initiator = initiator + 1

    total = data['header']['total_data']
    beat = total - dataSementara

    print 'Beat :{}'.format(beat)
    print 'sementara :{}'.format(dataSementara)
    print 'Total Produk :{}'.format(total)

    if(total > 200):
        if(beat < 1000 and beat > 800):
            return ambil(dataSementara+200,800)
        elif(beat < 800 and beat > 600):
            return ambil(dataSementara+200,600)
        elif(beat < 600 and beat > 400):
            return ambil(dataSementara+200,400)
        elif(beat < 400 and beat > 200):
            return ambil(dataSementara+200,200)
        elif(beat < 200):
            # if max(0, beat) == 0:
            print 'success'
            return exit
            # else :
            #     return ambil(dataSementara+200,200)
    return 'success'
    # print 'success'

ambil(0,0)
