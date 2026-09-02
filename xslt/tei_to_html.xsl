<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0"
                exclude-result-prefixes="tei">
  
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>
  
  <xsl:template match="/">
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        
        <title>
          <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
        </title>
        
        <style>
          * {
          box-sizing: border-box;
          }
          
          body {
          margin: 0;
          background: #ffffff;
          color: #202122;
          font-family: Arial, sans-serif;
          font-size: 16px;
          line-height: 1.6;
          }
          
          .page {
          max-width: 960px;
          margin: 0 auto;
          padding: 2.5rem 2rem 4rem;
          }
          
          header {
          margin-bottom: 2rem;
          }
          
          .project-label {
          margin: 0 0 0.35rem;
          color: #54595d;
          font-size: 0.85rem;
          text-transform: uppercase;
          }
          
          h1, h2 {
          color: #101418;
          font-family: Georgia, "Times New Roman", serif;
          font-weight: 400;
          line-height: 1.25;
          }
          
          h1 {
          margin: 0;
          padding-bottom: 0.25rem;
          border-bottom: 1px solid #a2a9b1;
          font-size: 2.25rem;
          }
          
          .encoding-title {
          margin: 0.65rem 0 0;
          color: #54595d;
          font-size: 0.95rem;
          }
          
          .source {
          margin: 0.35rem 0 0;
          color: #54595d;
          font-size: 0.9rem;
          }
          
          h2 {
          margin: 2.25rem 0 0.75rem;
          padding-bottom: 0.2rem;
          border-bottom: 1px solid #a2a9b1;
          font-size: 1.55rem;
          }
          
          h3 {
          margin: 1.75rem 0 0.6rem;
          color: #202122;
          font-family: Arial, sans-serif;
          font-size: 1.1rem;
          font-weight: 600;
          line-height: 1.4;
          }
          
          p {
          margin: 0.75rem 0;
          }
          
          a {
          color: #3366cc;
          text-decoration: none;
          }
          
          a:hover {
          text-decoration: underline;
          }
          
          .entity {
          color: #3366cc;
          border-bottom: 1px dotted #72777d;
          }
          
          .work {
          font-style: italic;
          }
          
          .quotation {
          font-style: italic;
          }
          
          .gap {
          margin: 1.5rem 0;
          color: #72777d;
          font-size: 0.9rem;
          text-align: center;
          }
          
          @media (max-width: 700px) {
          .page {
          padding: 1.5rem 1rem 3rem;
          }
          
          h1 {
          font-size: 1.9rem;
          }
          
          h2 {
          font-size: 1.4rem;
          }
          }
        </style>
      </head>
      
      <body>
        <div class="page">
          <header>
            <p class="project-label">00LOD · TEI/XML encoded sample</p>
            
            <!-- The title of the source work is used as the main heading of the HTML page. -->
            <h1>
              <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:title"/>
            </h1>
            
            <!-- The title of the TEI encoding is used as a subheading. -->
            <p class="encoding-title">
              <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
            </p>
            
            <p class="source">
              <xsl:text>Source: </xsl:text>
              
              <!-- The source URL is taken directly from the ptr/@target value in the TEI header. -->
              <a href="{tei:TEI/tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:ptr/@target}">
                <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:title"/>
              </a>
              
              <xsl:text> · accessed </xsl:text>
              <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:date[@type='accessed']"/>
            </p>
          </header>
          
          <main>
            <xsl:apply-templates select="tei:TEI/tei:text/tei:body/node()"/>
          </main>
        </div>
      </body>
    </html>
  </xsl:template>
  
  <!-- TEI divisions become HTML sections. -->
  <xsl:template match="tei:div">
    <section>
      <xsl:if test="@xml:id">
        <xsl:attribute name="id">
          <xsl:value-of select="@xml:id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
    </section>
  </xsl:template>
  
  <!-- The introductory head duplicates the main page title and is not rendered. -->
  <xsl:template match="tei:div[@xml:id='intro']/tei:head"/>
  
  <!-- Section and subsection headings are rendered at different HTML heading levels. -->
  <xsl:template match="tei:head">
    <xsl:choose>
      <xsl:when test="parent::tei:div[@type='subsection']">
        <h3><xsl:apply-templates/></h3>
      </xsl:when>
      <xsl:otherwise>
        <h2><xsl:apply-templates/></h2>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
  <xsl:template match="tei:p">
    <p><xsl:apply-templates/></p>
  </xsl:template>
  
  <!-- Inline textual markup. -->
  <xsl:template match="tei:emph">
    <em><xsl:apply-templates/></em>
  </xsl:template>
  
  <xsl:template match="tei:title">
    <span class="work"><xsl:apply-templates/></span>
  </xsl:template>
  
  <!-- Annotated entities are visually highlighted in the HTML output. -->
  <xsl:template match="tei:persName | tei:orgName | tei:objectName | tei:term | tei:rs | tei:num">
    <span class="entity"><xsl:apply-templates/></span>
  </xsl:template>
  
  <!-- The TEI source already contains quotation marks, so span is used instead of HTML q. -->
  <xsl:template match="tei:q">
    <span class="quotation"><xsl:apply-templates/></span>
  </xsl:template>
  
  <!-- Sampling omissions are made visible in the HTML output. -->
  <xsl:template match="tei:gap[@reason='sampling']">
    <p class="gap">--- omitted from the selected sample ---</p>
  </xsl:template>
  
  <!-- Nested name-part elements do not require additional HTML structure. -->
  <xsl:template match="tei:forename | tei:surname">
    <xsl:apply-templates/>
  </xsl:template>
  
  <!-- Fallback for TEI elements not explicitly transformed above. -->
  <xsl:template match="tei:*">
    <xsl:apply-templates/>
  </xsl:template>
  
</xsl:stylesheet>