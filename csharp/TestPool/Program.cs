using System;
using System.Collections;

using spiral.ga;


namespace TestPool
{
    public class Program
    {

        public static void TestGenome()
        {

        }

        public static void Main(string[] args)
        {
            Pool<NaturalNumberGenome> p = new Pool<NaturalNumberGenome>();

            NaturalNumberGenome.Max = 10;
            //NaturalNumberGenome.Test trial = new NaturalNumberGenome.Test(TestGenome);

            for (int i = 0; i < 100; i++)
            {
                p[i] = new NaturalNumberGenome(5);
                p[i].Create();

                //trial();
            }

            System.Console.ReadKey();
        }
    }
}
