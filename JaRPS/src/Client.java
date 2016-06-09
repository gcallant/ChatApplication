import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

/**
 * Created by Grant Callant. JaRPS
 *
 * @author Grant Callant
 */
public class Client extends Application implements Runnable
{
	private Socket    socket        = null;
	private TextField textFieldName = null;
	private TextField textFieldDestination = null;
	private TextField textFieldMessage = null;
	private TextArea  textArea      = null;
	private Button    buttonSend    = null, buttonClose = null;
	private Button setName = null;
	private String           destination      = "";
	private String           name             = "";
	private String message = "";
	private Thread           thread           = null;
	private DataOutputStream dataOutputStream = null;
	private DataInputStream  dataInputStream  = null;

	public Client()
	{


	}

	@Override
	public void start(Stage primaryStage) throws Exception
	{
		GridPane gridPane = new GridPane();
		gridPane.setPrefSize(700, 500);
		gridPane.setPadding(new Insets(10));
		gridPane.setHgap(5);
		gridPane.setVgap(5);

		textFieldName = new TextField();
		textFieldName.setPromptText("Enter your name");
		textFieldName.getText();
		GridPane.setConstraints(textFieldName, 0, 0);
		setName = new Button("Set Name");
		GridPane.setConstraints(setName, 1, 0);
		textFieldName.setPrefColumnCount(10);
		textFieldDestination = new TextField();
		textFieldDestination.setPromptText("Enter who you want to send to- or type everyone for broadcast");
		textFieldDestination.setPrefColumnCount(10);
		textFieldDestination.getText();
		GridPane.setConstraints(textFieldDestination, 0, 1);
		textArea = new TextArea();
		textArea.setPrefColumnCount(40);
		textArea.setPrefRowCount(20);
		textArea.setEditable(false);
		textArea.setWrapText(true);
		GridPane.setConstraints(textArea, 0, 4);
		textFieldMessage = new TextField();
		textFieldMessage.setPromptText("Enter your message");
		textFieldMessage.setPrefColumnCount(10);
		GridPane.setConstraints(textFieldMessage, 0, 5);
		buttonSend = new Button("Send");
		GridPane.setConstraints(buttonSend, 0, 7);
		buttonClose = new Button("Close");
		GridPane.setConstraints(buttonClose, 1, 7);

		setName.setOnAction(event ->
		                    {
			                    if(textFieldName.getText()!= null && !textFieldName.getText().isEmpty())
			                    {
				                    try
				                    {
					                    name = textFieldName.getText();
					                    textFieldName.setDisable(true);
					                    setName.setDisable(true);
					                    socket = new Socket("127.0.0.1", 34567);
					                    dataInputStream = new DataInputStream(socket.getInputStream());
					                    dataOutputStream = new DataOutputStream(socket.getOutputStream());
					                    dataOutputStream.writeUTF(name);
					                    thread = new Thread(this);
					                    thread.start();
				                    }
				                    catch(IOException e)
				                    {
					                    e.printStackTrace();
				                    }
			                    }
		                    });

		buttonSend.setOnAction(event ->
		                       {
			                       if(textFieldName.getText() != null && !textFieldName.getText().isEmpty()
					                            && textFieldDestination.getText() != null
					                            && textFieldMessage.getText() != null && !textFieldMessage.getText().isEmpty())
			                       {
				                       destination = textFieldDestination.getText();
				                       message = textFieldMessage.getText();
				                       try
				                       {
					                       dataOutputStream.writeUTF(destination + " " + "Message" + " " + name + " " + message);
					                       textArea.appendText("\n" + "You: " + message);
					                       textFieldMessage.setText("");
				                       }
				                       catch(IOException e)
				                       {
					                       e.printStackTrace();
				                       }
			                       }
		                       });
		buttonClose.setOnAction(event ->
		                        {
			                        try
			                        {
				                        dataOutputStream.writeUTF(name + " Quit" + " " + "Garbage" + " " + "Data"); //Text is necessary for string tokenizer- but parsing will stop once quit is parsed.
				                        System.exit(0);
			                        }
			                        catch(IOException e)
			                        {
				                        e.printStackTrace();
			                        }
		                        });

		gridPane.getChildren().addAll(textFieldName, setName, textFieldDestination, textArea, textFieldMessage, buttonSend, buttonClose);



		Scene scene = new Scene(gridPane);
		primaryStage.setScene(scene);
		primaryStage.setTitle(textFieldName.getText());
		primaryStage.show();
	}

	@Override
	public void run()
	{
		while(true)
		{
			try
			{
				textArea.appendText("\n" + dataInputStream.readUTF());
			}
			catch(IOException e)
			{
				e.printStackTrace();
			}
		}
	}
}
