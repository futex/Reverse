using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using dnlib.DotNet;
using dnlib.DotNet.MD;
using dnlib.DotNet.Emit;
using System.Security.Cryptography;
using System.IO;

namespace AgentTeslaStringsDecrypter
{
    public partial class Form1 : Form
    {
        string inputAssemblyName;

        public static string DecryptString(string str)
        {
            try
            {
                string strPassword = "amp4Z0wpKzJ5Cg0GDT5sJD0sMw0IDAsaGQ1Afik6NwXr6rrSEQE=";
                string s = "aGQ1Afik6NampDT5sJEQE4Z0wpsMw0IDAD06rrSswXrKzJ5Cg0G=";
                string strHashName = "SHA1";
                int iterations = 2;
                int num = 256;
                string s2 = "@1B2c3D4e5F6g7H8";
                byte[] bytes = Encoding.ASCII.GetBytes(s2);
                byte[] bytes2 = Encoding.ASCII.GetBytes(s);
                byte[] array = Convert.FromBase64String(str);
                PasswordDeriveBytes passwordDeriveBytes = new PasswordDeriveBytes(strPassword, bytes2, strHashName, iterations);
                byte[] bytes3 = passwordDeriveBytes.GetBytes(num / 8);
                ICryptoTransform transform = new RijndaelManaged
                {
                    Mode = CipherMode.CBC
                }.CreateDecryptor(bytes3, bytes);
                MemoryStream memoryStream = new MemoryStream(array);
                CryptoStream cryptoStream = new CryptoStream(memoryStream, transform, CryptoStreamMode.Read);
                byte[] array2 = new byte[array.Length];
                int count = cryptoStream.Read(array2, 0, array2.Length);
                memoryStream.Close();
                cryptoStream.Close();
                return Encoding.UTF8.GetString(array2, 0, count);
            }
            catch (Exception ex)
            {
               // if (ex.Source != null)
                // MessageBox.Show("DecryptString IOException source: {0}", ex.Message);

                return "null";
            }
        }

        public Form1()
        {
            InitializeComponent();
        }

        public static void DecryptStringsDnlib(String executable)
        {
            try
            {
                int count = 0;
                int countMethod = 0;
                int countModule = 0;

                string outputFolderName = Path.GetDirectoryName(executable);
                string filename = Path.GetFileNameWithoutExtension(executable);

                ModuleDefMD module = ModuleDefMD.Load(executable);

                foreach (TypeDef type in module.GetTypes())
                {
                    countModule++;

                    foreach (MethodDef method in type.Methods)
                    {
                        //if (!method.HasBody)
                        //   break;
                        if (!method.HasBody || method.IsConstructor)
                            continue;

                        countMethod++;

                        for (int i = 0; i < method.Body.Instructions.Count; i++)
                        {
                            if (method.Body.Instructions[i].OpCode.Value == 114) //OpCodes.Ldstr)
                            {
                                if (method.Body.Instructions[i + 1].OpCode == OpCodes.Call)
                                {
                                    var cryptedstring = method.Body.Instructions[i].Operand.ToString();

                                    string decryptedstring = DecryptString(cryptedstring);

                                    //For exception max stack value
                                    method.Body.KeepOldMaxStack = true;
                                    method.Body.Instructions[i].OpCode = OpCodes.Ldstr;
                                    method.Body.Instructions[i].Operand = decryptedstring;

                                    method.Body.Instructions.Remove(method.Body.Instructions[i + 1]);

                                    count++;
                                }
                            }
                        }
                    }
                }

               //MessageBox.Show("Total: " + count + " strings found." + " Number of methods: " + countMethod + " number of modules: " + countModule);

               String outputfilename = outputFolderName +" \\" + filename + "_uncrypt.exe";

               module.Write(outputfilename);

               MessageBox.Show("Clean sample write in: " + outputfilename + "\n" + count + " strings decrypted.");

            }
            catch (Exception ex)
            {
                if (ex.Source != null)
                    MessageBox.Show("DecryptStringsDnlib2 IOException source: {0}", ex.Message);
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
    
            if (openFileDialog1.ShowDialog() == DialogResult.OK) 
            {
                inputAssemblyName = openFileDialog1.FileName;
            }

        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (inputAssemblyName == null)
                MessageBox.Show("Select an assembly");
            else
                DecryptStringsDnlib(inputAssemblyName);
        }


    }
}
