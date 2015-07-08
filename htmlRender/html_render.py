#!/usr/bin/env python

# Base Element & Sub-classes

class Element(object):
    indent = '    '


    def __init__(self, tag, content, **kwargs):
        self.tag = tag
        self.contentList = []
        self.attributes = kwargs
        if content:
            self.append(content)


    def append(self, content):
        self.contentList.append(content)


    def render(self, file_out, indent = ""):
        # Render the open tag
        self.renderOpenTag(file_out, indent)        
        file_out.write('\n')        
        # Iterate through all content, rendering it recursively
        self.renderContent(file_out, indent)
        # Render close tag
        self.renderCloseTag(file_out, indent)
        if indent != '':
            file_out.write('\n')
        

    def renderOpenTag(self, file_out, indent = "", selfClosing = False):
        file_out.write(indent + '<' + self.tag);        
        for k, v in self.attributes.items():
            file_out.write(' ' + k + '="' + v + '"')
        if selfClosing:
            file_out.write(' />')
        else:
            file_out.write('>')


    def renderContent(self, file_out, indent = ""):
        for child in self.contentList:
            if isinstance(child, Element):
                # Render child elements
                child.render(file_out, indent + Element.indent)
            else:
                # Render string content
                file_out.write(indent + Element.indent + child + '\n')

    def renderCloseTag(self, file_out, indent = ""):
        file_out.write(indent + '</' + self.tag + '>')        
   

class Html(Element):

    def __init__(self, **kwargs):
        Element.__init__(self, 'html', '', **kwargs)

    def render(self, file_out, indent = ""):
        file_out.write('<!DOCTYPE html>\n')
        Element.render(self, file_out, indent)


class Body(Element):

    def __init__(self, **kwargs):
        Element.__init__(self, 'body', '', **kwargs)


class Head(Element):

    def __init__(self, **kwargs):
        Element.__init__(self, 'head', '', **kwargs)


class P(Element):

    def __init__(self, content = "", **kwargs):
        Element.__init__(self, 'p', content, **kwargs)


class Ul(Element):

    def __init__(self, **kwargs):
        Element.__init__(self, 'ul', '', **kwargs)


class Li(Element):

    def __init__(self, content = "", **kwargs):
        Element.__init__(self, 'li', content, **kwargs)


# OneLineTag Element & Sub-classes

class OneLineTag(Element):

    def __init__(self, tag, content = "", **kwargs):
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
        # TODO: I don't like the amount of logic that is re-implemented here - it's prone
        # to bugs down the road when render gets sufficiently complex. This should
        # really just call Element.render with some additional flags.
        Element.renderOpenTag(self, file_out, indent)
        for child in self.contentList:
            file_out.write(child)
        Element.renderCloseTag(self, file_out, '')
        file_out.write('\n')


class Title(OneLineTag):

    def __init__(self, content = "", **kwargs):
        OneLineTag.__init__(self, 'Title', content, **kwargs)


class A(OneLineTag):

    def __init__(self, link, content = "", **kwargs):
        kwargs['href'] = link
        OneLineTag.__init__(self, 'a', content, **kwargs)


class H(OneLineTag):

    def __init__(self, level, content = "", **kwargs):
        OneLineTag.__init__(self, 'h' + str(level), content, **kwargs)


# SelfClosingTag Element & Sub-classes

class SelfClosingTag(Element):

    def __init__(self, tag, **kwargs):
        Element.__init__(self, tag, '', **kwargs)


    def append(self, content):        
        raise Exception("Content cannot be set on a self closing tag element")


    def render(self, file_out, indent = ""):
        Element.renderOpenTag(self, file_out, indent, True)     
        file_out.write('\n')


class Hr(SelfClosingTag):

    def __init__(self, **kwargs):
        SelfClosingTag.__init__(self, 'hr', **kwargs)


class Br(SelfClosingTag):

    def __init__(self, **kwargs):
        SelfClosingTag.__init__(self, 'br', **kwargs)


class Meta(SelfClosingTag):

    def __init__(self, **kwargs):
        SelfClosingTag.__init__(self, 'meta', **kwargs)