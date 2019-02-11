package languagetoolEnglish;

import org.languagetool.language.AmericanEnglish;
import org.languagetool.rules.RuleMatch;

import java.io.IOException;
import java.util.List;

import org.languagetool.JLanguageTool;

import py4j.GatewayServer;

class Errors{
	
	private int style;
	private int others;

	public Errors() {
		super();
		this.style = 0;
		this.others = 0;
	}
	
	public int getStyleErrors(){
		return this.style;
	}
	
	public int getOthersErrors(){
		return this.others;
	}

	public void process(String txt){
		 
		JLanguageTool langTool = new JLanguageTool(new AmericanEnglish());
		
		try {
			List<RuleMatch> matches = langTool.check(txt);
			
			for (RuleMatch match : matches) {
				  String name = match.getRule().getCategory().getName();
				  if (name.equals("Style")){
					  this.style++;
				  }else{
					  this.others++;
				  }		  
			}
		} catch (IOException e) {
			System.out.println("Unable to check errors of the following string: " + txt);
			e.printStackTrace();
		}
	 }
}


public class ExtractErrors {
	
	 private Errors errors;
	 
	 public ExtractErrors() {
		    errors = new Errors();
			
	 }
	 
	 public Errors getErrors(){
		 return errors;
	 }
	 
	 public static void main(String[] args) {

		    GatewayServer server = new GatewayServer( new ExtractErrors());
		    System.out.println("Starting java server..");
	        server.start();
	 }
}
