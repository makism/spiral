using System;
using System.Collections.Generic;

using spiral.ga;

class MyIsland : Island<NaturalNumberGenome>
{
    public MyIsland()
        : base()
    {

    }

    public override void TestIndividual()
    {
        throw new NotImplementedException();
    }
}


namespace TestIsland
{
    public class Program
    {

        public static void Main(string[] args)
        {
            MyIsland myisland = new MyIsland();
            myisland.CreateInitial();
            /*Island<NaturalNumberGenome> island = new Island<NaturalNumberGenome>();
            Island<NaturalNumberGenome>.Test trial = new Island<NaturalNumberGenome>.Test(t);
            island[0] = new NaturalNumberGenome(10);
            trial();

            System.Console.WriteLine(island[0].ToString());
            System.Console.ReadKey();*/
        }

    }
}
