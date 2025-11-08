#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💈 نظام إدارة محل الحلاقة الرجالية
Barbershop Management System

نظام متكامل لإدارة محلات الحلاقة الرجالية
يشمل: المواعيد، العملاء، الحلاقين، الخدمات، التقارير

المطور: [Your Name]
الإصدار: 1.0.0
التاريخ: 2025-01-08
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
import os
import shutil
from pathlib import Path
import json

# ==================== الألوان والإعدادات ====================
COLORS = {
    # الألوان الرئيسية
    'primary': '#1a3a52',        # أزرق داكن
    'secondary': '#2d5270',      # أزرق متوسط
    'accent': '#d4af37',         # ذهبي

    # ألوان الحالات
    'success': '#10b981',        # أخضر
    'warning': '#f59e0b',        # برتقالي
    'danger': '#ef4444',         # أحمر
    'info': '#3b82f6',           # أزرق فاتح

    # ألوان الخلفيات
    'background': '#f5f5f5',     # رمادي فاتح جداً
    'card': '#ffffff',           # أبيض
    'sidebar': '#1a3a52',        # أزرق داكن

    # ألوان النصوص
    'text_dark': '#2c3e50',      # داكن
    'text_light': '#ecf0f1',     # فاتح
    'text_muted': '#6c757d',     # خافت

    # ألوان المواعيد
    'pending': '#f59e0b',        # معلق - برتقالي
    'confirmed': '#3b82f6',      # مؤكد - أزرق
    'completed': '#10b981',      # مكتمل - أخضر
    'cancelled': '#ef4444',      # ملغي - أحمر
    'no_show': '#94a3b8',        # غائب - رمادي
}

FONTS = {
    'family': 'Segoe UI',
    'title': 16,
    'subtitle': 14,
    'body': 11,
    'button': 11,
    'small': 9,
}

# ==================== الكلاس الرئيسي ====================
class BarbershopManagementSystem:
    def __init__(self, root):
        """تهيئة النظام"""
        self.root = root
        self.db_path = 'database/barbershop.db'

        # إنشاء المجلدات الضرورية
        self.create_folders()

        # إعداد النافذة الرئيسية
        self.setup_window()

        # إعداد قاعدة البيانات
        self.setup_database()

        # تحميل البيانات الافتراضية
        self.load_default_data()

        # بناء الواجهة الرئيسية
        self.create_main_interface()

        # تحديث الإحصائيات
        self.update_dashboard()

        # اختصارات لوحة المفاتيح
        self.setup_keyboard_shortcuts()

    def create_folders(self):
        """إنشاء المجلدات الضرورية"""
        folders = ['database', 'backups', 'exports', 'assets']
        for folder in folders:
            Path(folder).mkdir(exist_ok=True)
        print("✅ تم إنشاء المجلدات بنجاح")

    def setup_window(self):
        """إعداد النافذة الرئيسية"""
        self.root.title("💈 نظام إدارة محل الحلاقة")

        # حجم النافذة
        window_width = 1400
        window_height = 850

        # توسيط النافذة
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.root.configure(bg=COLORS['background'])

        # أيقونة النافذة (إذا كانت موجودة)
        try:
            self.root.iconbitmap('assets/icon.ico')
        except:
            pass

    def setup_database(self):
        """إنشاء قاعدة البيانات والجداول"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # جدول العملاء
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                email TEXT,
                birth_date DATE,
                address TEXT,
                preferences TEXT,
                loyalty_points INTEGER DEFAULT 0,
                total_visits INTEGER DEFAULT 0,
                total_spent REAL DEFAULT 0,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_visit DATETIME
            )
        ''')

        # جدول الحلاقين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS barbers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                hire_date DATE,
                specialization TEXT,
                commission_rate REAL DEFAULT 30,
                status TEXT DEFAULT 'active',
                working_days TEXT,
                working_hours TEXT,
                total_services INTEGER DEFAULT 0,
                total_revenue REAL DEFAULT 0,
                rating REAL DEFAULT 5.0,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # جدول الخدمات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                duration INTEGER NOT NULL,
                price REAL NOT NULL,
                cost REAL DEFAULT 0,
                commission_rate REAL,
                status TEXT DEFAULT 'active',
                popularity INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # جدول المواعيد
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                appointment_number TEXT UNIQUE NOT NULL,
                customer_id INTEGER,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                barber_id INTEGER NOT NULL,
                barber_name TEXT NOT NULL,
                service_id INTEGER NOT NULL,
                service_name TEXT NOT NULL,
                appointment_date DATE NOT NULL,
                appointment_time TIME NOT NULL,
                duration INTEGER,
                status TEXT DEFAULT 'pending',
                price REAL NOT NULL,
                cost REAL DEFAULT 0,
                commission REAL DEFAULT 0,
                payment_method TEXT,
                payment_status TEXT DEFAULT 'unpaid',
                rating INTEGER,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed_at DATETIME,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (barber_id) REFERENCES barbers(id),
                FOREIGN KEY (service_id) REFERENCES services(id)
            )
        ''')

        # جدول الجلسات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_number TEXT UNIQUE NOT NULL,
                customer_id INTEGER,
                customer_name TEXT NOT NULL,
                barber_id INTEGER NOT NULL,
                barber_name TEXT NOT NULL,
                services TEXT NOT NULL,
                total_price REAL NOT NULL,
                total_cost REAL DEFAULT 0,
                total_commission REAL DEFAULT 0,
                discount REAL DEFAULT 0,
                final_price REAL NOT NULL,
                payment_method TEXT NOT NULL,
                payment_status TEXT DEFAULT 'paid',
                loyalty_points_earned INTEGER DEFAULT 0,
                loyalty_points_used INTEGER DEFAULT 0,
                status TEXT DEFAULT 'completed',
                check_in_time DATETIME,
                check_out_time DATETIME,
                duration INTEGER,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (barber_id) REFERENCES barbers(id)
            )
        ''')

        # جدول الإعدادات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

        print("✅ تم إنشاء قاعدة البيانات بنجاح")

    def load_default_data(self):
        """تحميل البيانات الافتراضية (الخدمات والحلاقين)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # التحقق من وجود خدمات
        cursor.execute("SELECT COUNT(*) FROM services")
        if cursor.fetchone()[0] == 0:
            # تحميل الخدمات الافتراضية
            services = [
                # قص الشعر
                ('قص شعر عادي', 'قص شعر', 'قص شعر كلاسيكي بسيط', 30, 40, 5, 30, 'active'),
                ('قص شعر + تشكيل', 'قص شعر', 'قص شعر مع تشكيل الشعر', 40, 50, 6, 30, 'active'),
                ('قص شعر للأطفال', 'قص شعر', 'قص شعر للأطفال تحت 12 سنة', 25, 30, 4, 30, 'active'),
                ('قص شعر كلاسيكي', 'قص شعر', 'قص شعر بأسلوب كلاسيكي', 35, 45, 5, 30, 'active'),
                ('قص شعر حديث (Fade)', 'قص شعر', 'قص شعر حديث مع تدرج', 45, 60, 8, 35, 'active'),

                # حلاقة الذقن
                ('حلاقة ذقن عادية', 'حلاقة ذقن', 'حلاقة الذقن بشكل عادي', 20, 30, 3, 30, 'active'),
                ('حلاقة ذقن + تشذيب', 'حلاقة ذقن', 'حلاقة وتشذيب الذقن', 30, 40, 5, 30, 'active'),
                ('تشذيب الذقن فقط', 'حلاقة ذقن', 'تشذيب وتنظيف الذقن', 15, 25, 3, 30, 'active'),
                ('حلاقة ملكية', 'حلاقة ذقن', 'حلاقة فاخرة مع منشفة ساخنة', 40, 70, 10, 35, 'active'),

                # الصبغة
                ('صبغة شعر كاملة', 'صبغة', 'صبغة الشعر بالكامل', 90, 150, 40, 30, 'active'),
                ('صبغة شعر جزئية', 'صبغة', 'صبغة جزء من الشعر', 60, 100, 25, 30, 'active'),
                ('صبغة ذقن', 'صبغة', 'صبغة شعر الذقن', 45, 80, 20, 30, 'active'),
                ('إزالة الشيب', 'صبغة', 'إخفاء الشعر الأبيض', 75, 120, 30, 30, 'active'),

                # الباكجات
                ('باكج VIP', 'باكجات', 'قص شعر + حلاقة + تدليك', 90, 120, 20, 35, 'active'),
                ('باكج العريس', 'باكجات', 'باكج كامل للعريس', 120, 200, 40, 35, 'active'),
                ('باكج تجديد كامل', 'باكجات', 'قص + حلاقة + صبغة', 100, 180, 35, 35, 'active'),

                # خدمات إضافية
                ('غسيل الشعر', 'إضافية', 'غسيل وتنظيف الشعر', 10, 15, 2, 30, 'active'),
                ('تدليك الرأس', 'إضافية', 'تدليك فروة الرأس', 15, 25, 3, 30, 'active'),
                ('ماسك للشعر', 'إضافية', 'ماسك معالج للشعر', 20, 40, 8, 30, 'active'),
                ('تنظيف البشرة', 'إضافية', 'تنظيف عميق للبشرة', 30, 60, 10, 30, 'active'),
                ('تشقير الحواجب', 'إضافية', 'تشقير وتنظيف الحواجب', 20, 35, 5, 30, 'active'),
                ('حمام مغربي', 'إضافية', 'جلسة حمام مغربي', 60, 100, 20, 30, 'active'),
            ]

            cursor.executemany('''
                INSERT INTO services (name, category, description, duration, price, cost, commission_rate, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', services)

            print(f"✅ تم تحميل {len(services)} خدمة")

        # التحقق من وجود حلاقين
        cursor.execute("SELECT COUNT(*) FROM barbers")
        if cursor.fetchone()[0] == 0:
            # إضافة حلاق تجريبي
            cursor.execute('''
                INSERT INTO barbers (name, phone, specialization, commission_rate, status, working_days, working_hours)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('خالد محمد', '0501234567', 'قص شعر حديث', 35, 'active',
                  'السبت,الأحد,الاثنين,الثلاثاء,الأربعاء,الخميس', '09:00-18:00'))

            print("✅ تم إضافة حلاق تجريبي")

        # الإعدادات الافتراضية
        default_settings = [
            ('shop_name', 'محل الحلاقة'),
            ('shop_address', 'الرياض، المملكة العربية السعودية'),
            ('shop_phone', '0501234567'),
            ('shop_email', 'info@barbershop.com'),
            ('working_hours', '09:00-21:00'),
            ('tax_rate', '15'),
        ]

        for key, value in default_settings:
            cursor.execute('''
                INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)
            ''', (key, value))

        conn.commit()
        conn.close()

    def create_main_interface(self):
        """بناء الواجهة الرئيسية"""
        # الإطار الرئيسي
        main_frame = tk.Frame(self.root, bg=COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # شريط الإحصائيات العلوي
        self.create_stats_bar(main_frame)

        # الإطار الأوسط (نموذج الحجز + جدول المواعيد)
        middle_frame = tk.Frame(main_frame, bg=COLORS['background'])
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # نموذج الحجز السريع (يسار)
        self.create_booking_form(middle_frame)

        # جدول المواعيد (يمين)
        self.create_appointments_table(middle_frame)

        # أزرار الإجراءات السفلية
        self.create_action_buttons(main_frame)

    def create_stats_bar(self, parent):
        """إنشاء شريط الإحصائيات العلوي"""
        stats_frame = tk.Frame(parent, bg=COLORS['primary'], height=100)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        stats_frame.pack_propagate(False)

        # عنوان رئيسي
        title_label = tk.Label(
            stats_frame,
            text="💈 لوحة التحكم - إحصائيات اليوم",
            font=(FONTS['family'], FONTS['title'], 'bold'),
            bg=COLORS['primary'],
            fg=COLORS['text_light']
        )
        title_label.pack(pady=(10, 5))

        # إطار الإحصائيات
        stats_container = tk.Frame(stats_frame, bg=COLORS['primary'])
        stats_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        # الإحصائيات (4 أعمدة)
        self.stats_labels = {}
        stats_data = [
            ('customers_count', '👥 عملاء اليوم', '0'),
            ('revenue_today', '💰 الإيرادات', '0 ر.س'),
            ('appointments_count', '📅 المواعيد', '0'),
            ('profit_today', '💵 صافي الربح', '0 ر.س'),
        ]

        for i, (key, label_text, default_value) in enumerate(stats_data):
            stat_frame = tk.Frame(stats_container, bg=COLORS['primary'])
            stat_frame.grid(row=0, column=i, padx=15, sticky='ew')
            stats_container.columnconfigure(i, weight=1)

            # العنوان
            tk.Label(
                stat_frame,
                text=label_text,
                font=(FONTS['family'], FONTS['small']),
                bg=COLORS['primary'],
                fg=COLORS['text_light']
            ).pack()

            # القيمة
            value_label = tk.Label(
                stat_frame,
                text=default_value,
                font=(FONTS['family'], FONTS['subtitle'], 'bold'),
                bg=COLORS['primary'],
                fg=COLORS['accent']
            )
            value_label.pack()
            self.stats_labels[key] = value_label

    def create_booking_form(self, parent):
        """إنشاء نموذج الحجز السريع"""
        form_frame = tk.LabelFrame(
            parent,
            text="📋 حجز موعد جديد / جلسة سريعة",
            font=(FONTS['family'], FONTS['subtitle'], 'bold'),
            bg=COLORS['card'],
            fg=COLORS['text_dark'],
            relief=tk.RIDGE,
            bd=2
        )
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5), expand=True)

        # إطار داخلي للنموذج
        inner_frame = tk.Frame(form_frame, bg=COLORS['card'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # الحقول
        self.form_entries = {}

        # اسم العميل
        row = 0
        tk.Label(inner_frame, text="👤 اسم العميل:", bg=COLORS['card'],
                font=(FONTS['family'], FONTS['body'])).grid(row=row, column=0, sticky='w', pady=5)
        name_frame = tk.Frame(inner_frame, bg=COLORS['card'])
        name_frame.grid(row=row, column=1, sticky='ew', pady=5)
        self.form_entries['customer_name'] = tk.Entry(name_frame, font=(FONTS['family'], FONTS['body']), width=25)
        self.form_entries['customer_name'].pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(name_frame, text="🔍", command=self.search_customer,
                 bg=COLORS['info'], fg='white', width=3).pack(side=tk.LEFT, padx=(5, 0))

        # الجوال
        row += 1
        tk.Label(inner_frame, text="📱 الجوال:", bg=COLORS['card'],
                font=(FONTS['family'], FONTS['body'])).grid(row=row, column=0, sticky='w', pady=5)
        self.form_entries['phone'] = tk.Entry(inner_frame, font=(FONTS['family'], FONTS['body']), width=30)
        self.form_entries['phone'].grid(row=row, column=1, sticky='ew', pady=5)

        # الحلاق
        row += 1
        tk.Label(inner_frame, text="✂️ الحلاق:", bg=COLORS['card'],
                font=(FONTS['family'], FONTS['body'])).grid(row=row, column=0, sticky='w', pady=5)
        self.form_entries['barber'] = ttk.Combobox(inner_frame, font=(FONTS['family'], FONTS['body']),
                                                    state='readonly', width=28)
        self.form_entries['barber'].grid(row=row, column=1, sticky='ew', pady=5)
        self.load_barbers()

        # الخدمة
        row += 1
        tk.Label(inner_frame, text="💈 الخدمة:", bg=COLORS['card'],
                font=(FONTS['family'], FONTS['body'])).grid(row=row, column=0, sticky='w', pady=5)
        self.form_entries['service'] = ttk.Combobox(inner_frame, font=(FONTS['family'], FONTS['body']),
                                                     state='readonly', width=28)
        self.form_entries['service'].grid(row=row, column=1, sticky='ew', pady=5)
        self.form_entries['service'].bind('<<ComboboxSelected>>', self.on_service_selected)
        self.load_services()

        # التاريخ
        row += 1
        tk.Label(inner_frame, text="📅 التاريخ:", bg=COLORS['card'],
                font=(FONTS['family'], FONTS['body'])).grid(row=row, column=0, sticky='w', pady=5)
        self.form_entries['date'] = tk.Entry(inner_frame, font=(FONTS['family'], FONTS['body']), width=30)
        self.form_entries['date'].grid(row=row, column=1, sticky='ew', pady=5)
        self.form_entries['date'].insert(0, datetime.now().strftime('%Y-%m-%d'))

        # الوقت
        row += 1
        tk.Label(inner_frame, text="🕐 الوقت:", bg=COLORS['card'],
                font=(FONTS['family'], FONTS['body'])).grid(row=row, column=0, sticky='w', pady=5)
        self.form_entries['time'] = ttk.Combobox(inner_frame, font=(FONTS['family'], FONTS['body']),
                                                  state='readonly', width=28)
        self.form_entries['time'].grid(row=row, column=1, sticky='ew', pady=5)
        self.generate_time_slots()

        # السعر
        row += 1
        tk.Label(inner_frame, text="💰 السعر:", bg=COLORS['card'],
                font=(FONTS['family'], FONTS['body'])).grid(row=row, column=0, sticky='w', pady=5)
        price_frame = tk.Frame(inner_frame, bg=COLORS['card'])
        price_frame.grid(row=row, column=1, sticky='ew', pady=5)
        self.form_entries['price'] = tk.Entry(price_frame, font=(FONTS['family'], FONTS['body']), width=15)
        self.form_entries['price'].pack(side=tk.LEFT)
        tk.Label(price_frame, text="ر.س", bg=COLORS['card'],
                font=(FONTS['family'], FONTS['body'])).pack(side=tk.LEFT, padx=5)

        # طريقة الدفع
        row += 1
        tk.Label(inner_frame, text="💳 طريقة الدفع:", bg=COLORS['card'],
                font=(FONTS['family'], FONTS['body'])).grid(row=row, column=0, sticky='w', pady=5)
        self.form_entries['payment'] = ttk.Combobox(inner_frame, font=(FONTS['family'], FONTS['body']),
                                                     values=['نقدي', 'بطاقة', 'تحويل'],
                                                     state='readonly', width=28)
        self.form_entries['payment'].grid(row=row, column=1, sticky='ew', pady=5)
        self.form_entries['payment'].current(0)

        # ملاحظات
        row += 1
        tk.Label(inner_frame, text="📝 ملاحظات:", bg=COLORS['card'],
                font=(FONTS['family'], FONTS['body'])).grid(row=row, column=0, sticky='nw', pady=5)
        self.form_entries['notes'] = tk.Text(inner_frame, font=(FONTS['family'], FONTS['body']),
                                              width=30, height=3)
        self.form_entries['notes'].grid(row=row, column=1, sticky='ew', pady=5)

        # الأزرار
        row += 1
        buttons_frame = tk.Frame(inner_frame, bg=COLORS['card'])
        buttons_frame.grid(row=row, column=0, columnspan=2, pady=15)

        tk.Button(
            buttons_frame,
            text="💾 حفظ موعد",
            command=self.save_appointment,
            bg=COLORS['success'],
            fg='white',
            font=(FONTS['family'], FONTS['button'], 'bold'),
            cursor='hand2',
            width=15
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            buttons_frame,
            text="⚡ جلسة فورية",
            command=self.quick_session,
            bg=COLORS['warning'],
            fg='white',
            font=(FONTS['family'], FONTS['button'], 'bold'),
            cursor='hand2',
            width=15
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            buttons_frame,
            text="🗑️ مسح",
            command=self.clear_form,
            bg=COLORS['danger'],
            fg='white',
            font=(FONTS['family'], FONTS['button'], 'bold'),
            cursor='hand2',
            width=12
        ).pack(side=tk.LEFT, padx=5)

        # تكوين الأعمدة
        inner_frame.columnconfigure(1, weight=1)

    def create_appointments_table(self, parent):
        """إنشاء جدول المواعيد"""
        table_frame = tk.LabelFrame(
            parent,
            text="📋 مواعيد اليوم",
            font=(FONTS['family'], FONTS['subtitle'], 'bold'),
            bg=COLORS['card'],
            fg=COLORS['text_dark'],
            relief=tk.RIDGE,
            bd=2
        )
        table_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(5, 0), expand=True)

        # شريط البحث والفلترة
        search_frame = tk.Frame(table_frame, bg=COLORS['card'])
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(search_frame, text="🔍 بحث:", bg=COLORS['card'],
                font=(FONTS['family'], FONTS['body'])).pack(side=tk.LEFT, padx=(0, 5))

        self.search_entry = tk.Entry(search_frame, font=(FONTS['family'], FONTS['body']), width=25)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_appointments())

        tk.Button(
            search_frame,
            text="تحديث",
            command=self.load_appointments,
            bg=COLORS['info'],
            fg='white',
            font=(FONTS['family'], FONTS['small']),
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)

        # الجدول
        table_container = tk.Frame(table_frame, bg=COLORS['card'])
        table_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(table_container)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        x_scrollbar = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview
        columns = ('#', 'الوقت', 'العميل', 'الجوال', 'الحلاق', 'الخدمة', 'السعر', 'الحالة')
        self.appointments_tree = ttk.Treeview(
            table_container,
            columns=columns,
            show='headings',
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set,
            height=15
        )

        # تكوين الأعمدة
        widths = [40, 80, 120, 100, 100, 120, 80, 100]
        for col, width in zip(columns, widths):
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=width, anchor='center')

        self.appointments_tree.pack(fill=tk.BOTH, expand=True)

        y_scrollbar.config(command=self.appointments_tree.yview)
        x_scrollbar.config(command=self.appointments_tree.xview)

        # قائمة سياقية (Right-click menu)
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="✏️ تعديل", command=self.edit_appointment)
        self.context_menu.add_command(label="✅ تأكيد", command=self.confirm_appointment)
        self.context_menu.add_command(label="✔️ إنهاء", command=self.complete_appointment)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="❌ إلغاء", command=self.cancel_appointment)
        self.context_menu.add_command(label="🗑️ حذف", command=self.delete_appointment)

        self.appointments_tree.bind('<Button-3>', self.show_context_menu)
        self.appointments_tree.bind('<Double-1>', lambda e: self.edit_appointment())

        # تلوين الصفوف حسب الحالة
        self.appointments_tree.tag_configure('pending', background='#fff3cd')
        self.appointments_tree.tag_configure('confirmed', background='#d1ecf1')
        self.appointments_tree.tag_configure('completed', background='#d4edda')
        self.appointments_tree.tag_configure('cancelled', background='#f8d7da')

    def create_action_buttons(self, parent):
        """إنشاء أزرار الإجراءات السفلية"""
        buttons_frame = tk.Frame(parent, bg=COLORS['background'])
        buttons_frame.pack(fill=tk.X, pady=(10, 0))

        # صف 1 من الأزرار
        row1_frame = tk.Frame(buttons_frame, bg=COLORS['background'])
        row1_frame.pack(fill=tk.X, pady=(0, 5))

        buttons_row1 = [
            ("👥 العملاء", self.open_customers_window, COLORS['info']),
            ("✂️ الحلاقين", self.open_barbers_window, COLORS['info']),
            ("💈 الخدمات", self.open_services_window, COLORS['info']),
            ("📊 التقارير", self.open_reports_window, COLORS['secondary']),
        ]

        for text, command, color in buttons_row1:
            tk.Button(
                row1_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=(FONTS['family'], FONTS['button'], 'bold'),
                cursor='hand2',
                width=18,
                height=2
            ).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # صف 2 من الأزرار
        row2_frame = tk.Frame(buttons_frame, bg=COLORS['background'])
        row2_frame.pack(fill=tk.X)

        buttons_row2 = [
            ("⚙️ الإعدادات", self.open_settings_window, COLORS['text_muted']),
            ("📤 تصدير Excel", self.export_to_excel, COLORS['success']),
            ("💾 نسخ احتياطي", self.backup_database, COLORS['warning']),
            ("❌ خروج", self.exit_app, COLORS['danger']),
        ]

        for text, command, color in buttons_row2:
            tk.Button(
                row2_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=(FONTS['family'], FONTS['button'], 'bold'),
                cursor='hand2',
                width=18,
                height=2
            ).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

    # ==================== دوال مساعدة للنموذج ====================

    def load_barbers(self):
        """تحميل قائمة الحلاقين"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM barbers WHERE status='active' ORDER BY name")
            barbers = cursor.fetchall()
            conn.close()

            barber_list = [f"{b[1]} (#{b[0]})" for b in barbers]
            self.form_entries['barber']['values'] = barber_list
            if barber_list:
                self.form_entries['barber'].current(0)
        except Exception as e:
            print(f"خطأ في تحميل الحلاقين: {e}")

    def load_services(self):
        """تحميل قائمة الخدمات"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, price FROM services WHERE status='active' ORDER BY category, name")
            services = cursor.fetchall()
            conn.close()

            service_list = [f"{s[1]} - {s[2]} ر.س (#{s[0]})" for s in services]
            self.form_entries['service']['values'] = service_list
        except Exception as e:
            print(f"خطأ في تحميل الخدمات: {e}")

    def generate_time_slots(self):
        """إنشاء فتحات الوقت"""
        time_slots = []
        for hour in range(9, 21):  # من 9 صباحاً إلى 9 مساءً
            for minute in ['00', '30']:
                time_slots.append(f"{hour:02d}:{minute}")
        self.form_entries['time']['values'] = time_slots

    def on_service_selected(self, event=None):
        """عند اختيار خدمة - تحديث السعر تلقائياً"""
        try:
            service_text = self.form_entries['service'].get()
            if service_text:
                # استخراج معرف الخدمة
                service_id = int(service_text.split('#')[-1].strip(')'))

                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT price FROM services WHERE id=?", (service_id,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    self.form_entries['price'].delete(0, tk.END)
                    self.form_entries['price'].insert(0, str(result[0]))
        except Exception as e:
            print(f"خطأ في تحديث السعر: {e}")

    def search_customer(self):
        """البحث عن عميل موجود"""
        search_window = tk.Toplevel(self.root)
        search_window.title("🔍 البحث عن عميل")
        search_window.geometry("600x400")
        search_window.configure(bg=COLORS['background'])

        # حقل البحث
        search_frame = tk.Frame(search_window, bg=COLORS['background'])
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(search_frame, text="البحث:", bg=COLORS['background']).pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame, font=(FONTS['family'], FONTS['body']), width=30)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # جدول النتائج
        columns = ('الاسم', 'الجوال', 'الزيارات', 'النقاط')
        tree = ttk.Treeview(search_window, columns=columns, show='headings', height=12)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor='center')

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def search_customers(event=None):
            search_text = search_entry.get()
            tree.delete(*tree.get_children())

            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT name, phone, total_visits, loyalty_points
                    FROM customers
                    WHERE name LIKE ? OR phone LIKE ?
                    ORDER BY name
                """, (f'%{search_text}%', f'%{search_text}%'))

                for row in cursor.fetchall():
                    tree.insert('', 'end', values=row)

                conn.close()
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل البحث:\n{e}")

        def select_customer(event=None):
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                values = item['values']

                self.form_entries['customer_name'].delete(0, tk.END)
                self.form_entries['customer_name'].insert(0, values[0])

                self.form_entries['phone'].delete(0, tk.END)
                self.form_entries['phone'].insert(0, values[1])

                search_window.destroy()

        search_entry.bind('<KeyRelease>', search_customers)
        tree.bind('<Double-1>', select_customer)

        # زر الاختيار
        tk.Button(
            search_window,
            text="اختيار",
            command=select_customer,
            bg=COLORS['success'],
            fg='white',
            font=(FONTS['family'], FONTS['button']),
            cursor='hand2'
        ).pack(pady=10)

        search_customers()

    def clear_form(self):
        """مسح النموذج"""
        for key, entry in self.form_entries.items():
            if key in ['customer_name', 'phone', 'price']:
                entry.delete(0, tk.END)
            elif key == 'notes':
                entry.delete('1.0', tk.END)
            elif key == 'date':
                entry.delete(0, tk.END)
                entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

        if self.form_entries['barber']['values']:
            self.form_entries['barber'].current(0)

        self.form_entries['payment'].current(0)

    # ==================== دوال المواعيد ====================

    def generate_appointment_number(self):
        """توليد رقم موعد تلقائي"""
        today = datetime.now().strftime('%Y%m%d')

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM appointments
                WHERE appointment_number LIKE ?
            ''', (f'APP-{today}%',))
            count = cursor.fetchone()[0] + 1
            conn.close()

            return f'APP-{today}-{count:03d}'
        except Exception as e:
            print(f"خطأ في توليد رقم الموعد: {e}")
            return f'APP-{today}-001'

    def save_appointment(self):
        """حفظ موعد جديد"""
        try:
            # التحقق من الحقول المطلوبة
            customer_name = self.form_entries['customer_name'].get().strip()
            phone = self.form_entries['phone'].get().strip()
            barber = self.form_entries['barber'].get()
            service = self.form_entries['service'].get()
            app_date = self.form_entries['date'].get().strip()
            app_time = self.form_entries['time'].get()
            price = self.form_entries['price'].get().strip()

            if not all([customer_name, phone, barber, service, app_date, app_time, price]):
                messagebox.showwarning("تحذير", "الرجاء ملء جميع الحقول المطلوبة!")
                return

            # استخراج المعرفات
            barber_id = int(barber.split('#')[-1].strip(')'))
            barber_name = barber.split('(#')[0].strip()

            service_id = int(service.split('#')[-1].strip(')'))
            service_name = service.split(' - ')[0].strip()

            # توليد رقم الموعد
            app_number = self.generate_appointment_number()

            # الحصول على بيانات إضافية
            payment_method = self.form_entries['payment'].get()
            notes = self.form_entries['notes'].get('1.0', tk.END).strip()

            # البحث عن العميل أو إضافته
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM customers WHERE phone=?", (phone,))
            customer = cursor.fetchone()

            if customer:
                customer_id = customer[0]
            else:
                # إضافة عميل جديد
                cursor.execute("""
                    INSERT INTO customers (name, phone)
                    VALUES (?, ?)
                """, (customer_name, phone))
                customer_id = cursor.lastrowid

            # الحصول على معلومات الخدمة
            cursor.execute("SELECT duration, cost, commission_rate FROM services WHERE id=?", (service_id,))
            service_data = cursor.fetchone()
            duration = service_data[0]
            cost = service_data[1]

            # حساب العمولة
            cursor.execute("SELECT commission_rate FROM barbers WHERE id=?", (barber_id,))
            barber_commission_rate = cursor.fetchone()[0]
            commission_rate = service_data[2] if service_data[2] else barber_commission_rate
            commission = float(price) * (commission_rate / 100)

            # إضافة الموعد
            cursor.execute("""
                INSERT INTO appointments (
                    appointment_number, customer_id, customer_name, phone,
                    barber_id, barber_name, service_id, service_name,
                    appointment_date, appointment_time, duration,
                    status, price, cost, commission, payment_method, notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?, ?, ?, ?)
            """, (app_number, customer_id, customer_name, phone,
                  barber_id, barber_name, service_id, service_name,
                  app_date, app_time, duration, price, cost, commission,
                  payment_method, notes))

            conn.commit()
            conn.close()

            messagebox.showinfo("نجح", f"✅ تم حجز الموعد بنجاح!\nرقم الموعد: {app_number}")

            self.clear_form()
            self.load_appointments()
            self.update_dashboard()

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل حفظ الموعد:\n{e}")

    def quick_session(self):
        """جلسة سريعة (بدون موعد مسبق)"""
        # نفس التحقق من البيانات
        try:
            customer_name = self.form_entries['customer_name'].get().strip()
            phone = self.form_entries['phone'].get().strip()
            barber = self.form_entries['barber'].get()
            service = self.form_entries['service'].get()
            price = self.form_entries['price'].get().strip()
            payment_method = self.form_entries['payment'].get()

            if not all([customer_name, phone, barber, service, price]):
                messagebox.showwarning("تحذير", "الرجاء ملء جميع الحقول المطلوبة!")
                return

            # استخراج المعرفات
            barber_id = int(barber.split('#')[-1].strip(')'))
            barber_name = barber.split('(#')[0].strip()

            service_id = int(service.split('#')[-1].strip(')'))
            service_name = service.split(' - ')[0].strip()

            # توليد رقم الجلسة
            today = datetime.now().strftime('%Y%m%d')
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sessions WHERE session_number LIKE ?", (f'SES-{today}%',))
            count = cursor.fetchone()[0] + 1
            session_number = f'SES-{today}-{count:03d}'

            # البحث عن العميل أو إضافته
            cursor.execute("SELECT id, loyalty_points FROM customers WHERE phone=?", (phone,))
            customer = cursor.fetchone()

            if customer:
                customer_id = customer[0]
                loyalty_points = customer[1]
            else:
                cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer_name, phone))
                customer_id = cursor.lastrowid
                loyalty_points = 0

            # حساب النقاط المكتسبة (كل 10 ريال = 1 نقطة)
            points_earned = int(float(price) * 0.1)

            # الحصول على تكلفة الخدمة
            cursor.execute("SELECT cost, commission_rate FROM services WHERE id=?", (service_id,))
            service_data = cursor.fetchone()
            cost = service_data[0]

            # حساب العمولة
            cursor.execute("SELECT commission_rate FROM barbers WHERE id=?", (barber_id,))
            barber_commission_rate = cursor.fetchone()[0]
            commission_rate = service_data[1] if service_data[1] else barber_commission_rate
            commission = float(price) * (commission_rate / 100)

            # إضافة الجلسة
            services_json = json.dumps([{
                'id': service_id,
                'name': service_name,
                'price': float(price)
            }])

            cursor.execute("""
                INSERT INTO sessions (
                    session_number, customer_id, customer_name, barber_id, barber_name,
                    services, total_price, total_cost, total_commission,
                    discount, final_price, payment_method, loyalty_points_earned,
                    check_in_time, check_out_time, status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?, ?, ?, 'completed')
            """, (session_number, customer_id, customer_name, barber_id, barber_name,
                  services_json, float(price), cost, commission, float(price),
                  payment_method, points_earned, datetime.now(), datetime.now()))

            # تحديث بيانات العميل
            cursor.execute("""
                UPDATE customers
                SET loyalty_points = loyalty_points + ?,
                    total_visits = total_visits + 1,
                    total_spent = total_spent + ?,
                    last_visit = ?
                WHERE id = ?
            """, (points_earned, float(price), datetime.now(), customer_id))

            # تحديث بيانات الحلاق
            cursor.execute("""
                UPDATE barbers
                SET total_services = total_services + 1,
                    total_revenue = total_revenue + ?
                WHERE id = ?
            """, (float(price), barber_id))

            conn.commit()
            conn.close()

            messagebox.showinfo("نجح",
                f"✅ تمت الجلسة بنجاح!\n"
                f"رقم الجلسة: {session_number}\n"
                f"النقاط المكتسبة: {points_earned} نقطة\n"
                f"إجمالي النقاط: {loyalty_points + points_earned}")

            self.clear_form()
            self.update_dashboard()

        except Exception as e:
            messagebox.showerror("خطأ", f"فشلت الجلسة:\n{e}")

    def load_appointments(self):
        """تحميل المواعيد"""
        try:
            # مسح الجدول
            for item in self.appointments_tree.get_children():
                self.appointments_tree.delete(item)

            # الحصول على نص البحث
            search_text = self.search_entry.get() if hasattr(self, 'search_entry') else ''

            # الاستعلام
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            today = datetime.now().strftime('%Y-%m-%d')

            query = """
                SELECT id, appointment_time, customer_name, phone, barber_name,
                       service_name, price, status
                FROM appointments
                WHERE appointment_date = ?
            """
            params = [today]

            if search_text:
                query += """ AND (customer_name LIKE ? OR phone LIKE ?
                            OR appointment_number LIKE ?)"""
                params.extend([f'%{search_text}%', f'%{search_text}%', f'%{search_text}%'])

            query += " ORDER BY appointment_time"

            cursor.execute(query, params)
            appointments = cursor.fetchall()
            conn.close()

            # عرض المواعيد
            status_map = {
                'pending': 'معلق',
                'confirmed': 'مؤكد',
                'completed': 'مكتمل',
                'cancelled': 'ملغي',
                'no_show': 'غائب'
            }

            for i, app in enumerate(appointments, 1):
                values = (
                    i,
                    app[1],  # الوقت
                    app[2],  # العميل
                    app[3],  # الجوال
                    app[4],  # الحلاق
                    app[5],  # الخدمة
                    f"{app[6]} ر.س",  # السعر
                    status_map.get(app[7], app[7])  # الحالة
                )

                item_id = self.appointments_tree.insert('', 'end', values=values, iid=str(app[0]))
                self.appointments_tree.item(item_id, tags=(app[7],))

        except Exception as e:
            print(f"خطأ في تحميل المواعيد: {e}")

    def show_context_menu(self, event):
        """عرض القائمة السياقية"""
        try:
            self.appointments_tree.selection_set(self.appointments_tree.identify_row(event.y))
            self.context_menu.post(event.x_root, event.y_root)
        except:
            pass

    def edit_appointment(self):
        """تعديل موعد"""
        selection = self.appointments_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "الرجاء اختيار موعد أولاً!")
            return

        # TODO: نافذة تعديل الموعد
        messagebox.showinfo("قريباً", "ميزة التعديل قيد التطوير")

    def confirm_appointment(self):
        """تأكيد موعد"""
        selection = self.appointments_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "الرجاء اختيار موعد أولاً!")
            return

        try:
            app_id = int(selection[0])

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE appointments SET status='confirmed' WHERE id=?", (app_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("نجح", "✅ تم تأكيد الموعد")
            self.load_appointments()

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل التأكيد:\n{e}")

    def complete_appointment(self):
        """إنهاء موعد"""
        selection = self.appointments_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "الرجاء اختيار موعد أولاً!")
            return

        try:
            app_id = int(selection[0])

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # الحصول على بيانات الموعد
            cursor.execute("""
                SELECT customer_id, price, payment_status
                FROM appointments WHERE id=?
            """, (app_id,))
            app_data = cursor.fetchone()

            if not app_data:
                raise Exception("الموعد غير موجود")

            customer_id, price, payment_status = app_data

            # تحديث حالة الموعد
            cursor.execute("""
                UPDATE appointments
                SET status='completed', completed_at=?, payment_status='paid'
                WHERE id=?
            """, (datetime.now(), app_id))

            # تحديث بيانات العميل
            if customer_id:
                points_earned = int(float(price) * 0.1)
                cursor.execute("""
                    UPDATE customers
                    SET total_visits = total_visits + 1,
                        total_spent = total_spent + ?,
                        loyalty_points = loyalty_points + ?,
                        last_visit = ?
                    WHERE id = ?
                """, (float(price), points_earned, datetime.now(), customer_id))

            conn.commit()
            conn.close()

            messagebox.showinfo("نجح", "✅ تم إنهاء الموعد بنجاح!")
            self.load_appointments()
            self.update_dashboard()

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل إنهاء الموعد:\n{e}")

    def cancel_appointment(self):
        """إلغاء موعد"""
        selection = self.appointments_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "الرجاء اختيار موعد أولاً!")
            return

        if messagebox.askyesno("تأكيد", "هل أنت متأكد من إلغاء الموعد؟"):
            try:
                app_id = int(selection[0])

                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("UPDATE appointments SET status='cancelled' WHERE id=?", (app_id,))
                conn.commit()
                conn.close()

                messagebox.showinfo("نجح", "✅ تم إلغاء الموعد")
                self.load_appointments()
                self.update_dashboard()

            except Exception as e:
                messagebox.showerror("خطأ", f"فشل الإلغاء:\n{e}")

    def delete_appointment(self):
        """حذف موعد"""
        selection = self.appointments_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "الرجاء اختيار موعد أولاً!")
            return

        if messagebox.askyesno("تأكيد", "⚠️ هل أنت متأكد من حذف الموعد نهائياً؟"):
            try:
                app_id = int(selection[0])

                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM appointments WHERE id=?", (app_id,))
                conn.commit()
                conn.close()

                messagebox.showinfo("نجح", "✅ تم حذف الموعد")
                self.load_appointments()
                self.update_dashboard()

            except Exception as e:
                messagebox.showerror("خطأ", f"فشل الحذف:\n{e}")

    def update_dashboard(self):
        """تحديث إحصائيات لوحة التحكم"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            today = datetime.now().strftime('%Y-%m-%d')

            # عدد العملاء اليوم
            cursor.execute("""
                SELECT COUNT(DISTINCT customer_id)
                FROM appointments
                WHERE appointment_date = ? AND status != 'cancelled'
            """, (today,))
            customers_count = cursor.fetchone()[0]

            # الإيرادات اليومية
            cursor.execute("""
                SELECT COALESCE(SUM(price), 0)
                FROM appointments
                WHERE appointment_date = ? AND status = 'completed'
            """, (today,))
            revenue = cursor.fetchone()[0]

            # عدد المواعيد
            cursor.execute("""
                SELECT COUNT(*)
                FROM appointments
                WHERE appointment_date = ?
            """, (today,))
            appointments_count = cursor.fetchone()[0]

            # صافي الربح (الإيرادات - التكاليف - العمولات)
            cursor.execute("""
                SELECT COALESCE(SUM(price - cost - commission), 0)
                FROM appointments
                WHERE appointment_date = ? AND status = 'completed'
            """, (today,))
            profit = cursor.fetchone()[0]

            conn.close()

            # تحديث الواجهة
            self.stats_labels['customers_count'].config(text=str(customers_count))
            self.stats_labels['revenue_today'].config(text=f"{revenue:,.0f} ر.س")
            self.stats_labels['appointments_count'].config(text=str(appointments_count))
            self.stats_labels['profit_today'].config(text=f"{profit:,.0f} ر.س")

        except Exception as e:
            print(f"خطأ في تحديث الإحصائيات: {e}")

    # ==================== نوافذ الإدارة ====================

    def open_customers_window(self):
        """نافذة إدارة العملاء"""
        messagebox.showinfo("قريباً", "نافذة إدارة العملاء قيد التطوير")

    def open_barbers_window(self):
        """نافذة إدارة الحلاقين"""
        messagebox.showinfo("قريباً", "نافذة إدارة الحلاقين قيد التطوير")

    def open_services_window(self):
        """نافذة إدارة الخدمات"""
        messagebox.showinfo("قريباً", "نافذة إدارة الخدمات قيد التطوير")

    def open_reports_window(self):
        """نافذة التقارير"""
        messagebox.showinfo("قريباً", "نافذة التقارير قيد التطوير")

    def open_settings_window(self):
        """نافذة الإعدادات"""
        messagebox.showinfo("قريباً", "نافذة الإعدادات قيد التطوير")

    # ==================== التصدير والنسخ الاحتياطي ====================

    def export_to_excel(self):
        """تصدير إلى Excel"""
        try:
            # اختيار مكان الحفظ
            filename = filedialog.asksaveasfilename(
                defaultextension='.xlsx',
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"appointments_{datetime.now().strftime('%Y%m%d')}.xlsx"
            )

            if not filename:
                return

            # الحصول على البيانات
            conn = sqlite3.connect(self.db_path)

            # المواعيد
            df_appointments = pd.read_sql_query("""
                SELECT
                    appointment_number as 'رقم الموعد',
                    customer_name as 'العميل',
                    phone as 'الجوال',
                    barber_name as 'الحلاق',
                    service_name as 'الخدمة',
                    appointment_date as 'التاريخ',
                    appointment_time as 'الوقت',
                    price as 'السعر',
                    status as 'الحالة',
                    payment_method as 'طريقة الدفع'
                FROM appointments
                WHERE appointment_date = ?
                ORDER BY appointment_time
            """, conn, params=[datetime.now().strftime('%Y-%m-%d')])

            conn.close()

            # الكتابة إلى Excel
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df_appointments.to_excel(writer, sheet_name='المواعيد', index=False)

                # تنسيق
                worksheet = writer.sheets['المواعيد']
                for column in worksheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

            messagebox.showinfo("نجح", f"✅ تم التصدير بنجاح!\n{filename}")

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل التصدير:\n{e}")

    def backup_database(self):
        """نسخ احتياطي لقاعدة البيانات"""
        try:
            # إنشاء اسم ملف النسخة
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = f'backups/backup_{timestamp}.db'

            # نسخ قاعدة البيانات
            shutil.copy2(self.db_path, backup_file)

            # حذف النسخ القديمة (الاحتفاظ بآخر 30 نسخة)
            backups = sorted(Path('backups').glob('*.db'))
            if len(backups) > 30:
                for old_backup in backups[:-30]:
                    old_backup.unlink()

            messagebox.showinfo("نجح", f"✅ تم إنشاء نسخة احتياطية:\n{backup_file}")

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل النسخ الاحتياطي:\n{e}")

    # ==================== اختصارات لوحة المفاتيح ====================

    def setup_keyboard_shortcuts(self):
        """إعداد اختصارات لوحة المفاتيح"""
        self.root.bind('<Control-n>', lambda e: self.form_entries['customer_name'].focus())
        self.root.bind('<Control-q>', lambda e: self.quick_session())
        self.root.bind('<Control-s>', lambda e: self.save_appointment())
        self.root.bind('<Control-f>', lambda e: self.search_entry.focus() if hasattr(self, 'search_entry') else None)
        self.root.bind('<Control-c>', lambda e: self.open_customers_window())
        self.root.bind('<Control-b>', lambda e: self.open_barbers_window())
        self.root.bind('<Control-m>', lambda e: self.open_services_window())
        self.root.bind('<Control-r>', lambda e: self.open_reports_window())
        self.root.bind('<Control-e>', lambda e: self.export_to_excel())
        self.root.bind('<Control-d>', lambda e: self.backup_database())
        self.root.bind('<F5>', lambda e: self.load_appointments())
        self.root.bind('<Delete>', lambda e: self.delete_appointment())
        self.root.bind('<Escape>', lambda e: self.clear_form())

    def exit_app(self):
        """الخروج من التطبيق"""
        if messagebox.askyesno("تأكيد الخروج", "هل أنت متأكد من الخروج؟"):
            self.root.quit()


# ==================== نقطة البداية ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = BarbershopManagementSystem(root)
    root.mainloop()
