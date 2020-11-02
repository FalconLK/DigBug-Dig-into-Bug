#!/usr/bin/env python
# -*- coding: utf-8 -*-

from JavaASTVisitor import JavaASTVisitor
from org.eclipse.jdt.core.dom import ASTParser, AST, ASTNode, ASTVisitor, MethodDeclaration, CompilationUnit
from java.lang import String

class TestVisitor(ASTVisitor):
	def __init__(self):
		self.result = None

	def visit(self, node):
		# print "VISIT", type(node)
		# if isinstance(node, CompilationUnit):
		# 	return True

		if isinstance(node, MethodDeclaration):
			self.result = 2
			return False
		return True

class JavaParser:

	def __init__(self, resolve):
		self.resolve = resolve
		self.flag = 0
		self.cutype = 0
	
	  	# cutype =  0 => already has class body and method body
	  	# 			1 => has tmp method wrapper but no class
	  	# 			2 => missing both method and class wrapper (just tmp bunch of statements)
	 

	def getASTParser(self, sourceCode, parserType):
		parser = ASTParser.newParser(AST.JLS3);
		# print "RESOLVE", self.resolve
		
		parser.setSource(String(sourceCode).toCharArray())
		parser.setResolveBindings(self.resolve);
		parser.setStatementsRecovery(self.resolve);
		parser.setBindingsRecovery(self.resolve);
		parser.setKind(parserType)
		return parser


	def getCompilationUnitFromString(self, code):
		parser = self.getASTParser(code, ASTParser.K_COMPILATION_UNIT)
		cu = parser.createAST(None)
		self.cutype = 0

		if cu.types().isEmpty():
			self.flag = 1
			self.cutype = 1
			s1 = "public class MyJDTWrapperClass{\n %s \n}" % code
			parser = self.getASTParser(s1, ASTParser.K_COMPILATION_UNIT)
			cu = parser.createAST(None)
			v = TestVisitor()
			cu.accept(v)
			if v.result:
				self.flag = v.result

			#print "CODE", s1

			if self.flag == 1:
				s1 = "public class MyJDTWrapperClass{\n public void MyJDTWrapperMethod(){\n %s \n}\n}" % code
				self.cutype = 2
				parser = self.getASTParser(s1, ASTParser.K_COMPILATION_UNIT)
				cu = parser.createAST(None)
			if self.flag == 2:
				s1 = "public class MyJDTWrapperClass{\n %s \n}" % code
				self.cutype = 1
				parser = self.getASTParser(s1, ASTParser.K_COMPILATION_UNIT)
				cu = parser.createAST(None)
		else:
			self.cutype = 0
			parser = self.getASTParser(code, ASTParser.K_COMPILATION_UNIT)
			cu = parser.createAST(None)

		s1 = s1 if self.cutype != 0 else code
		return cu, s1

def parse(code, resolve=False, source=False):
	try:
		parser = JavaParser(resolve)
		cu, s1 = parser.getCompilationUnitFromString(code)
	
		v = JavaASTVisitor(cu, s1)

	
		cu.accept(v)
	except:
		print "Parser error!"	
		return None


	if source:
		return v.get_AST(), s1


	return v.get_AST()


if __name__ == '__main__':

	source1 = """ 
	package jm.org.data.area;

import com.google.analytics.tracking.android.EasyTracker;

import android.app.ActionBar;
import android.app.SearchManager;
import android.content.Context;
import android.os.Build;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.widget.SearchView;

public class ReportViewActivity extends BaseActivity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.report_view);

		if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.HONEYCOMB) {
			// only for android newer than gingerbread
			ActionBar actionBar = getActionBar();
			actionBar.setDisplayHomeAsUpEnabled(true);
		}
	}
	
	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		MenuInflater menuInflater = getMenuInflater();
		menuInflater.inflate(R.menu.home, menu);

		if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.HONEYCOMB) {
			// only for android newer than gingerbread
			// TODO Implement tmp Search Dialog fall back for compatibility with
			// Android 2.3 and lower
			// Currently crashes on Gingerbread or lower

			// Get the SearchView and set the searchable configuration
			SearchManager searchManager = (SearchManager) getSystemService(Context.SEARCH_SERVICE);
			SearchView searchView = (SearchView) menu
					.findItem(R.id.menu_search).getActionView();
			searchView.setSearchableInfo(searchManager
					.getSearchableInfo(getComponentName()));
			searchView.setIconifiedByDefault(true); // Do not iconify the
													// widget; expand it by
													// default
		}
		return super.onCreateOptionsMenu(menu);
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) {
		case android.R.id.home:
			finish();
			return true;
		default:
			return super.onOptionsItemSelected(item);
		}

	}
	
	@Override
	public void onStart() {
		super.onStart();
		
		EasyTracker.getInstance(this).activityStart(this);  // Add this method.
		}
	
	@Override
	public void onStop() {
		super.onStop();
	
		EasyTracker.getInstance(this).activityStop(this);  // Add this method.
	}
}
	"""

	source11 = """
	package de.uni.stuttgart.informatik.ToureNPlaner.Net.Handler;

import android.graphics.RectF;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import de.uni.stuttgart.informatik.ToureNPlaner.Net.JacksonManager;
import de.uni.stuttgart.informatik.ToureNPlaner.Net.Observer;
import de.uni.stuttgart.informatik.ToureNPlaner.ToureNPlanerApplication;
import org.mapsforge.core.GeoPoint;

import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;

public class NominatimHandler extends GeoCodingHandler {
	private final String query;
	private final RectF viewbox;

	private static final String HOST = "http://nominatim.openstreetmap.org/search?format=json&limit=1";

	public NominatimHandler(Observer listener, String query, RectF viewbox) {
		super(listener);
		this.query = query;
		this.viewbox = viewbox;
	}

	@Override
	protected HttpURLConnection getHttpUrlConnection() throws Exception {
		URL url = new URL(HOST +
				"&q=" + URLEncoder.encode(query, "UTF-8") +
				"&viewbox=" + viewbox.left + "," + viewbox.top + "," + viewbox.right + "," + viewbox.bottom);
		HttpURLConnection connection = (HttpURLConnection) url.openConnection();
		connection.setRequestProperty("User-Agent", "Android " + ToureNPlanerApplication.getApplicationIdentifier());
		return connection;
	}

	@Override
	protected void handleOutput(OutputStream connection) throws Exception {}

	@Override
	protected Object handleInput(JacksonManager.ContentType type, InputStream inputStream) throws Exception {
		ObjectMapper mapper = JacksonManager.getMapper(type);
		JsonNode node = mapper.readValue(inputStream, JsonNode.class);
		GeoCodingResult result = new GeoCodingResult();

		result.location = new GeoPoint(
				node.get(0).get("lat").asDouble(),
				node.get(0).get("lon").asDouble());

		return result;
	}
}


	 """

	source2 = """ 
	View.OnClickListener mStartButtonListener = new OnClickListener() {
        @Override
        public void onClick(View arg0) {
            mChronometer.setBase(SystemClock.elapsedRealtime());
            mChronometer.start();
        }
    };
	"""

	source11 = """public class Main {
  public static void main(String[] args) {
    /* Total number of processors or cores available to the JVM */
    System.out.println("Available processors (cores): " + 
        Runtime.getRuntime().availableProcessors());

    /* Total amount of free memory available to the JVM */
    System.out.println("Free memory (bytes): " + 
        Runtime.getRuntime().freeMemory());

    /* This will return Long.MAX_VALUE if there is no preset limit */
    long maxMemory = Runtime.getRuntime().maxMemory();
    /* Maximum amount of memory the JVM will attempt to use */
    System.out.println("Maximum memory (bytes): " + 
        (maxMemory == Long.MAX_VALUE ? "no limit" : maxMemory));

    /* Total memory currently available to the JVM */
    System.out.println("Total memory available to JVM (bytes): " + 
        Runtime.getRuntime().totalMemory());

    /* Get tmp list of all filesystem roots on this system */
    File[] roots = File.listRoots();

    /* For each filesystem root, print some info */
    for (File root : roots) {
      System.out.println("File system root: " + root.getAbsolutePath());
      System.out.println("Total space (bytes): " + root.getTotalSpace());
      System.out.println("Free space (bytes): " + root.getFreeSpace());
      System.out.println("Usable space (bytes): " + root.getUsableSpace());
    }
  }
} """


	source11 = """import javax.xml.XMLConstants;
import javax.xml.transform.Source;
import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.*;
//...

URL schemaFile = new URL("http://java.sun.com/xml/ns/j2ee/web-app_2_4.xsd");
Source xmlFile = new StreamSource(new File("web.xml"));
SchemaFactory schemaFactory = SchemaFactory
    .newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
Schema schema = schemaFactory.newSchema(schemaFile);
Validator validator = schema.newValidator();
try {
  validator.validate(xmlFile);
  System.out.println(xmlFile.getSystemId() + " is valid");
} catch (SAXException e) {
  System.out.println(xmlFile.getSystemId() + " is NOT valid");
  System.out.println("Reason: " + e.getLocalizedMessage());
} """
	
	

	ast = parse(source11, resolve=True)

	

	# print "FQN"

	# # Create Map from Simple Type -> FQN Type 
	# # For Example: Activity -> android.view.Activity
	# class_fqn_map = { im.split(".")[-1]: im for im in ast["imports"] if im.split(".")[-1] != "*" }
	# print class_fqn_map
	# print "Used_classes", ast["used_classes"]

	# fqnm_list = []
	# method_fqn_type_map = {}
	# # Create Map from Typed Method Name -> FQN Method
	# # Example: Menu.findItem ->  android.view.Menu.findItem
	# for tmc in ast["typed_method_call"]:
	# 	class_name, method_name = tmc.split(".")
	# 	if class_name in class_fqn_map:
	# 		print tmc, tmc.replace(class_name, class_fqn_map[class_name], 1)

	# 		fqnm = tmc.replace(class_name, class_fqn_map[class_name], 1) # Replace only first occurrence
	# 		fqnm_list.append( fqnm ) 

	# 		method_fqn_type_map[method_name] = {}
	# 		method_fqn_type_map[method_name]["fqn"] = fqnm
	# 		method_fqn_type_map[method_name]["class"] = class_fqn_map[class_name]

	# print "method_fqn_type_map", method_fqn_type_map
	# # Case we match only tmp method_call 1. determine FQNM 2. assign variable name to FQN


	# print ast

	# print "----"*10


	# ast = parse(source2, resolve=True)
	# print "Snippet PART"

	# # convert partial qualified named variables to fully qualified names
	# # Example: 
	# for var, var_type in ast["var_type_map"].iteritems():
	# 	# In case PQN is prefixed by some identifier
	# 	if "." in var_type:
	# 		parts = var_type.split(".")
	# 		# Get Suffix
	# 		suffixed_var_type = parts[-1]
	# 		prefixed_var_type = parts[0]
	# 		if suffixed_var_type in class_fqn_map:
	# 			ast["var_type_map"][var] = class_fqn_map[suffixed_var_type]
	# 		elif prefixed_var_type in class_fqn_map:
	# 			ast["var_type_map"][var] = class_fqn_map[prefixed_var_type] + "." + ".".join(parts[1:])
	# 	else:
	# 		if var_type in class_fqn_map:
	# 			ast["var_type_map"][var] = class_fqn_map[var_type]
			
	# 	if var not in ast["var_type_map"]:
	# 		print "Could not resolve: %s, %s" %  (var_type ,var)



	# # Resolved untyped variables
	# for umc in ast["unresolved_method_calls"]:
	# 	unresolved_var, method_name = umc.split(".")

	# 	if method_name in method_fqn_type_map:
	# 		print unresolved_var, method_name,  method_fqn_type_map[method_name]["class"]

	# 		ast["var_type_map"][unresolved_var] = method_fqn_type_map[method_name]["class"]
	# 	else:
	# 		"Could not resolve: %s" % unresolved_var

	# # Resolve untyped method calls
	# for method_name in ast["methods_called"]:
	# 	if method_name in method_fqn_type_map:

	# 		print method_name, method_fqn_type_map[method_name]["fqn"]
	# 	else:
	# 		"Could not resolve: %s" % method_name

	
	print ast
