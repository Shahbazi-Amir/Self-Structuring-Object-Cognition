import networkx as nx
import re
import unicodedata

class AristotelianLogic:
    def __init__(self):
        # گراف دانش برای ذخیره مفاهیم و روابط
        self.knowledge_graph = nx.DiGraph()
        # لیست جملات برای تشخیص تناقض
        self.statements = []

    def normalize_text(self, text):
        """نرمال‌سازی متن برای مدیریت نیم‌فاصله و کاراکترهای خاص"""
        text = text.replace("\u200c", " ")  # تبدیل نیم‌فاصله به فاصله
        text = unicodedata.normalize('NFKC', text)  # نرمال‌سازی یونیکد
        return text.strip()

    def add_universal_affirmative(self, subject, predicate):
        """اضافه کردن جمله‌ی 'همه S، P هستند'"""
        subject = self.normalize_text(subject)
        predicate = self.normalize_text(predicate)
        self.knowledge_graph.add_node(subject, type="subject")
        self.knowledge_graph.add_node(predicate, type="predicate")
        self.knowledge_graph.add_edge(subject, predicate, quantifier="همه")
        self.statements.append((subject, predicate, "همه"))

    def add_universal_negative(self, subject, predicate):
        """اضافه کردن جمله‌ی 'هیچ S، P نیست'"""
        subject = self.normalize_text(subject)
        predicate = self.normalize_text(predicate)
        self.knowledge_graph.add_node(subject, type="subject")
        self.knowledge_graph.add_node(predicate, type="predicate")
        self.knowledge_graph.add_edge(subject, predicate, quantifier="هیچکدام")
        self.statements.append((subject, predicate, "هیچکدام"))

    def add_particular_affirmative(self, subject, predicate):
        """اضافه کردن جمله‌ی 'بعضی S، P هستند'"""
        subject = self.normalize_text(subject)
        predicate = self.normalize_text(predicate)
        self.knowledge_graph.add_node(subject, type="subject")
        self.knowledge_graph.add_node(predicate, type="predicate")
        self.knowledge_graph.add_edge(subject, predicate, quantifier="بعضی")
        self.statements.append((subject, predicate, "بعضی"))

    def add_particular_negative(self, subject, predicate):
        """اضافه کردن جمله‌ی 'بعضی S، P نیستند'"""
        subject = self.normalize_text(subject)
        predicate = self.normalize_text(predicate)
        self.knowledge_graph.add_node(subject, type="subject")
        self.knowledge_graph.add_node(predicate, type="predicate")
        self.knowledge_graph.add_edge(subject, predicate, quantifier="بعضی_نه")
        self.statements.append((subject, predicate, "بعضی_نه"))

    def add_instance(self, instance, category):
        """اضافه کردن نمونه، مثلاً 'سقراط انسان است'"""
        instance = self.normalize_text(instance)
        category = self.normalize_text(category)
        self.knowledge_graph.add_node(instance, type="instance")
        self.knowledge_graph.add_node(category, type="category")
        self.knowledge_graph.add_edge(instance, category, quantifier="است")
        self.statements.append((instance, category, "است"))

    def infer(self, subject, predicate):
        """استدلال برای فهمیدن اینکه آیا subject predicate است یا نه"""
        subject = self.normalize_text(subject)
        predicate = self.normalize_text(predicate)

        # بررسی وجود گره‌ها
        if not self.knowledge_graph.has_node(subject) or not self.knowledge_graph.has_node(predicate):
            return f"نتیجه‌گیری ممکن نیست: گره {subject} یا {predicate} در گراف وجود ندارد."

        # بررسی مستقیم
        if self.knowledge_graph.has_edge(subject, predicate):
            quantifier = self.knowledge_graph[subject][predicate]["quantifier"]
            if quantifier in ["همه", "است"]:
                return f"{subject} {predicate} است."
            elif quantifier == "بعضی":
                return f"بعضی {subject} {predicate} است."
            elif quantifier == "هیچکدام":
                return f"{subject} {predicate} نیست."
            elif quantifier == "بعضی_نه":
                return f"بعضی {subject} {predicate} نیستند."

        # استدلال غیرمستقیم (سیلوژیسم)
        for node in self.knowledge_graph.predecessors(predicate):
            edge_data = self.knowledge_graph[node][predicate]
            if edge_data["quantifier"] == "همه":
                if self.knowledge_graph.has_edge(subject, node) and \
                   self.knowledge_graph[subject][node]["quantifier"] in ["است", "همه"]:
                    return f"{subject} {predicate} است."
            elif edge_data["quantifier"] == "هیچکدام":
                if self.knowledge_graph.has_edge(subject, node) and \
                   self.knowledge_graph[subject][node]["quantifier"] in ["است", "همه"]:
                    return f"{subject} {predicate} نیست."

        return "نتیجه‌گیری ممکن نیست."

    def check_contradiction(self):
        """تشخیص تناقض در جملات موجود"""
        for i, stmt1 in enumerate(self.statements):
            for stmt2 in self.statements[i+1:]:
                if stmt1[0] == stmt2[0] and stmt1[1] == stmt2[1]:
                    if (stmt1[2] == "همه" and stmt2[2] == "هیچکدام") or \
                       (stmt1[2] == "همه" and stmt2[2] == "بعضی_نه") or \
                       (stmt1[2] == "بعضی" and stmt2[2] == "هیچکدام"):
                        return f"تناقض یافت شد: {stmt1[0]} {stmt1[1]} {stmt1[2]} و {stmt2[0]} {stmt2[1]} {stmt2[2]}"
        return "تناقضی یافت نشد."

    def process_input(self, input_str):
        """پردازش ورودی متنی و اضافه کردن به گراف"""
        input_str = self.normalize_text(input_str)
        
        # الگوهای بهبودیافته برای تجزیه ورودی
        patterns = [
            (r"همه\s+([^\s]+)\s+(.+?)(?:\s+هستند)?$", self.add_universal_affirmative),
            (r"هیچ\s+([^\s]+(?:\s+[^\s]+)?)\s+(.+?)(?:\s+نیست)?$", self.add_universal_negative),
            (r"بعضی\s+([^\s]+)\s+(.+?)(?:\s+هستند)?$", self.add_particular_affirmative),
            (r"بعضی\s+([^\s]+)\s+(.+?)(?:\s+نیستند)?$", self.add_particular_negative),
            (r"([^\s]+)\s+([^\s]+)(?:\s+است)?$", self.add_instance),
        ]
        
        for pattern, func in patterns:
            match = re.match(pattern, input_str)
            if match:
                subject, predicate = match.groups()
                func(subject.strip(), predicate.strip())
                return f"اضافه شد: {input_str}"
        
        return f"ورودی قابل تشخیص نیست: {input_str}"

    def get_graph_info(self):
        """دیباگ: نمایش گره‌ها و روابط گراف"""
        nodes = list(self.knowledge_graph.nodes(data=True))
        edges = list(self.knowledge_graph.edges(data=True))
        return f"گره‌ها: {nodes}\nروابط: {edges}"

# مثال استفاده
if __name__ == "__main__":
    logic = AristotelianLogic()
    inputs = [
        "همه پرندگان پرواز می‌کنند",
        "کبوتر پرنده است",
        "هیچ پرنده‌ای پستاندار نیست",
        "بعضی پرندگان پرواز نمی‌کنند"
    ]
    for input_str in inputs:
        print(logic.process_input(input_str))
        print(logic.get_graph_info())
    print(logic.infer("کبوتر", "پرواز می‌کنند"))
    print(logic.check_contradiction())