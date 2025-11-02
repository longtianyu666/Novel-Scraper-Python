import tkinter
import logging
import threading
import webbrowser
from tkinter import ttk,messagebox 
import Scrape_linovelib

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s:%(message)s')
liNovelLib_catalog_url='https://www.linovelib.com/novel/{lib_novel_id}/catalog'
class NovelScrapeApp:
    def __init__(self,master:tkinter.Tk):
        # 网站
        self.link_url='https://www.linovelib.com/'
        
        self.master=master
        master.title('NovelScrape')
        master.geometry('1000x650')
        
        self.isScraping=False
        
        self.idLabel=ttk.Label(master,text='小说ID')
        self.idLabel.grid(row=0,column=0,padx=10,pady=5,sticky='w')
        
        self.link_label=ttk.Label(
            master,
            text='访问哔哩轻小说主页',
            foreground='blue',
            font=('TkDefaultFont', 9, 'underline'),
            cursor='hand2'
        )
        
        self.link_label.grid(row=0,column=2,padx=10,pady=5,sticky='w')
        self.link_label.bind('<Button-1>',self.open_link)
        
        self.link_label_2=ttk.Label(
            master,
            text='直接访问目录',
            foreground='blue',
            font=('TkDefaultFont', 9, 'underline'),
            cursor='hand2'
        )
        
        self.link_label_2.grid(row=1,column=2,padx=10,pady=5,sticky='w')
        self.link_label_2.bind('<Button-1>',self.open_link_2)
        # 输入框
        self.idEntry=ttk.Entry(master)
        self.idEntry.grid(row=0,column=1,padx=10,pady=5,sticky='ew')
        # 按钮
        self.scrapButton=ttk.Button(master,text='开始爬取',command=self.start_scrape_thread)
        self.scrapButton.grid(row=1,column=0,columnspan=2,padx=3,pady=3,sticky='ew')
        # 状态栏
        self.status_var=tkinter.StringVar()
        self.status_var.set('等待输入....')
        self.status_label=ttk.Label(master,textvariable=self.status_var,relief=tkinter.SUNKEN,anchor='w')
        self.status_label.grid(row=2,column=0,columnspan=2,sticky='ew')
        master.grid_columnconfigure(1,weight=1)
        # 日志
        log_frame=ttk.LabelFrame(master,text='爬取日志')
        log_frame.grid(row=3,column=0,columnspan=2,padx=10,pady=10,sticky='nsew')
        # 日志文本框
        log_scrollbar=ttk.Scrollbar(log_frame)
        log_scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        
        self.log_text=tkinter.Text(
            log_frame,
            height=20,
            width=30,
            wrap='word',
            yscrollcommand=log_scrollbar.set,
            state='disabled',
            font=('consolas',11,'normal')
        )
        
        self.log_text.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True,padx=5,pady=5)
        log_scrollbar.config(command=self.log_text.yview)
        
        master.grid_rowconfigure(4,weight=1)
        log_frame.grid_columnconfigure(0,weight=1)
        # 日志处理
        root_logger=logging.getLogger()
        text_handler=TextHandler(self.log_text)
        text_handler.setLevel(logging.INFO)
        # 添加处理器
        root_logger.addHandler(text_handler)
        root_logger.setLevel(logging.INFO)
        # 增量更新
        self.input_catalog_button=ttk.Button(master,text='输入html',command=self.input_catalog_html)
        self.input_catalog_button.grid(row=2,column=2,padx=3,pady=3,sticky='e')
        
        self.incremental_update_button=ttk.Button(master,text='增量更新',command=self.incremental_update_by_id)
        self.incremental_update_button.grid(row=3,column=2,padx=3,pady=3,sticky='e')
        
    def start_scrape_thread(self):
        # 判断爬虫是否正在运行
        if self.isScraping:
            messagebox.showwarning('警告','爬虫正在运行中，请等候完成')
            return
        novel_id_str=self.idEntry.get().strip()
        
        if not novel_id_str.isdigit():
            messagebox.showerror('错误','小说ID必须为数字')
            return
        novel_id=int(novel_id_str)
        
        self.isScraping=True
        self.status_var.set('爬虫执行中...')
        self.scrapButton.config(state=tkinter.DISABLED,text='正在爬取...')
        
        thread=threading.Thread(target=self.run_scraper,args=(novel_id,))
        thread.start()
        
    def run_scraper(self,novel_id): 
        
        try:
            message=Scrape_linovelib.start_scrape(novel_id,None,False)
            self.master.after(0,self.update_gui_after_scrape,True,message)
        except Exception as e:
            logging.error(f'线程中异常:{e}')
            self.master.after(0,self.update_gui_after_scrape,False,f'线程中异常:{e}')
    
    def update_gui_after_scrape(self,success,message):
        self.isScraping=False
        self.scrapButton.config(state=tkinter.NORMAL,text='开始爬取')
        self.input_catalog_button.config(state=tkinter.NORMAL)
        
        if success:
            self.status_var.set(f'执行成功:{message}')
            messagebox.showinfo('完成',message)
        else:
            self.status_var.set(f'执行失败:{message}')
            messagebox.showerror('错误',message)

    def input_catalog_html(self):
        if self.isScraping:
            messagebox.showerror('警告','爬虫正在运行中，请等候完成')
            return
        
        dialog=tkinter.Toplevel(self.master)
        dialog.title('自定义输入目录html')
        dialog.geometry('800x1000')
        
        dialog.transient(self.master)
        
        text_frame=ttk.Frame(dialog)
        text_frame.pack(fill='both',expand=True,padx=10,pady=5)
        
        ttk.Label(dialog,text='在此粘贴目录html').pack(padx=10,pady=5,anchor='w')
        scroll_bar=ttk.Scrollbar(text_frame,orient=tkinter.VERTICAL)
        scroll_bar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        self.html_text=tkinter.Text(
            text_frame,
            height=30,
            width=50,
            wrap='word',
            font=('Consolas',11,'normal'),
            yscrollcommand=scroll_bar.set
        )
        self.html_text.pack(fill='both',expand=True,padx=10,pady=5)
        scroll_bar.config(command=self.html_text.yview)
        def submit_html():
            html_content=self.html_text.get('1.0',tkinter.END).strip()
            if not html_content:
                messagebox.showerror('警告','未输入html,请输入html',parent=dialog)
                return
            
            dialog.destroy()
            
            self.isScraping=True
            self.status_var.set('正在解析html')
            self.scrapButton.config(state=tkinter.DISABLED,text='正在爬取...')
            self.input_catalog_button.config(state=tkinter.DISABLED)
            
            thread=threading.Thread(target=self.run_manual_scraper,args=(html_content,))
            thread.start()
            
        submit_button=ttk.Button(dialog,text='解析输入内容',command=submit_html)
        submit_button.pack(pady=10)
        
        incremental_button=ttk.Button(dialog,text='增量更新',command=self.incremental_update_by_html)
        incremental_button.pack(pady=10)
        
        
        dialog.grab_set()
        self.master.wait_window(dialog)
            
    def run_manual_scraper(self, catalog_html):
        try:
            message = Scrape_linovelib.start_scrape(0, catalog_html,False) 
            self.master.after(0, self.update_gui_after_scrape, True, message)
        except Exception as e:
            logging.error(f'线程中异常:{e}')
            self.master.after(0, self.update_gui_after_scrape, False, f'线程中异常:{e}')
            
    def open_link(self,event):
        try:
            logging.info(f'尝试打开链接:{self.link_url}')
            webbrowser.open_new_tab(self.link_url)
        except Exception as e:
            messagebox.showerror("打开链接失败", f"无法打开网页: {self.link_url}\n错误: {e}")
    def open_link_2(self,event):
        try:
            novel_id=self.idEntry.get().strip()
            if novel_id:
                url=liNovelLib_catalog_url.format(lib_novel_id=novel_id)
                logging.info(f'尝试打开链接:{url}')
                webbrowser.open_new_tab(url)
            else:
                messagebox.showerror('警告','没有输入id')
        except Exception as e:
            messagebox.showerror("打开链接失败", f"无法打开网页: {url}\n错误: {e}")
        
    def incremental_update_by_id(self):
        if self.isScraping:
            messagebox.showwarning('警告', '爬虫正在运行中，请等候完成')
            return
        novel_id=self.idEntry.get().strip()
        
        if not novel_id.isdigit():
            messagebox.showerror('错误','小说ID必须为数字')
            return
        novel_id=int(novel_id)
        
        self.isScraping=True
        self.status_var.set('增量更新执行中...')
        self.incremental_update_button.config(state=tkinter.DISABLED)
        self.scrapButton.config(state=tkinter.DISABLED,text='正在更新')
        self.input_catalog_button.config(state=tkinter.DISABLED)
        
        thread=threading.Thread(target=self.run_incremental_scraper,args=(novel_id,None))
        thread.start()
    def incremental_update_by_html(self):
        if self.isScraping:
            messagebox.showwarning('警告', '爬虫正在运行中，请等候完成')
            return
        catalog=self.html_text.get('1.0',tkinter.END).strip()
        
        if not catalog:
            messagebox.showerror('错误','html不能为空')
            return

        self.isScraping=True
        self.status_var.set('增量更新执行中...')
        self.incremental_update_button.config(state=tkinter.DISABLED)
        self.scrapButton.config(state=tkinter.DISABLED,text='正在更新')
        self.input_catalog_button.config(state=tkinter.DISABLED)
        
        thread=threading.Thread(target=self.run_incremental_scraper,args=(0,catalog))
        thread.start()

    def run_incremental_scraper(self,novel_id,catalog):
        try:
            if novel_id:
                message = Scrape_linovelib.start_scrape(novel_id, None,True)
            else:
                message=Scrape_linovelib.start_scrape(0,catalog,True)
            self.master.after(0, self.update_gui_after_scrape, True, message)
        except Exception as e:
            logging.error(f'线程中异常:{e}')
            self.master.after(0, self.update_gui_after_scrape, False, f'线程中异常:{e}')

class TextHandler(logging.Handler):
    def __init__(self:logging.Handler,text_widget):
        super().__init__()
        self.text_widget=text_widget
        formatter=logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        self.setFormatter(formatter)
    
    def emit(self,record):
        msg=self.format(record)
        def append_log():
            self.text_widget.config(state='normal')
            self.text_widget.insert(tkinter.END,msg+'\n')
            self.text_widget.see(tkinter.END)
            self.text_widget.config(state='disabled')
        self.text_widget.after(0,append_log)

if __name__=='__main__':
    root=tkinter.Tk()
    app=NovelScrapeApp(root)
    root.mainloop()