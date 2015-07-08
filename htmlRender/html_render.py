#!/usr/bin/env python

class Element(object):
    indent = '    '


    def __init__(self, tag, content, **kwargs):
        self.tag = tag
        self.content = ''
        self.childElements = []
        self.attributes = kwargs
        self.append(content)


    def append(self, content):
        if isinstance(content, Element):
            self.childElements.append(content)
        else:
            self.content += content


    def render(self, file_out, indent = ""):
        # Render the open tag
        self.renderOpenTag(file_out, indent)        
        file_out.write('\n')
        # Iterate through all child elements, rendering them recursively
        for child in self.childElements:
            child.render(file_out, indent + Element.indent)
        # Render string content
        if self.content != '':
            file_out.write(indent + Element.indent + self.content + '\n')            
        # Render close tag
        self.renderCloseTag(file_out, indent)
        if indent != '':
            file_out.write('\n')
        

    def renderOpenTag(self, file_out, indent = ""):
        file_out.write(indent + '<' + self.tag);
        for k, v in self.attributes.items():
            file_out.write(' ' + k + '="' + v + '"')
        file_out.write('>')


    def renderCloseTag(self, file_out, indent = ""):
        file_out.write(indent + '</' + self.tag + '>')        
   

class Html(Element):

    def __init__(self, **kwargs):
        Element.__init__(self, 'html', '', **kwargs)


class Body(Element):

    def __init__(self, **kwargs):
        Element.__init__(self, 'body', '', **kwargs)


class Head(Element):

    def __init__(self, **kwargs):
        Element.__init__(self, 'head', '', **kwargs)


class P(Element):

    def __init__(self, content, **kwargs):
        Element.__init__(self, 'p', content, **kwargs)


class OneLineTag(Element):

    def __init__(self, tag, content, **kwargs):
        Element.__init__(self, tag, content, **kwargs)


    def append(self, content):
        # The assignment instructs us to override the render method in order to implement
        # the OneLineTag element. In doing that, we're bypassing the recursion logic in the 
        # base class which is responsible for iterating through the child elements. 
        # Presumably, this element type is not intended for non-string content, so we're
        # explicitly disallowing it here.
        if not isinstance(content, str):
            raise Exception("OneLineTag content must be a string")
        Element.append(self, content)


    def render(self, file_out, indent = ""):
        Element.renderOpenTag(self, file_out, indent)
        file_out.write(self.content)
        Element.renderCloseTag(self, file_out, '')
        file_out.write('\n')


class Title(OneLineTag):

    def __init__(self, content, **kwargs):
        OneLineTag.__init__(self, 'Title', content, **kwargs)