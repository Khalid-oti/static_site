class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("HTML NOT IMPLEMENTED")

    def props_to_html(self):
        if self.props == None:
            return ""
        attribute_string = ""
        for attribute in self.props:
            attribute_string += f' {attribute}="{self.props[attribute]}"'
        return attribute_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, other):
        return (
            self.tag == other.tag 
            and self.value == other.value 
            and self.children == other.children 
            and self.props == other.props
        )
        

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("VALUE NOT FOUND")
        elif self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("TAG NOT FOUND")
        if self.children == None:
            raise ValueError("CHILD NOT FOUND")
        html_children = ""
        for child in self.children:
            html_children += child.to_html()        
        return f"<{self.tag}{self.props_to_html()}>{html_children}</{self.tag}>"

            