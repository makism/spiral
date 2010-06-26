using System;
using System.Collections;


namespace spiral.ga
{
    public class NaturalNumberGenome: Genome<int>
    {
        #region Max/Min/Padding members/properties
        private static int max = Int32.MaxValue;
        private static int min = (int)UInt32.MinValue;
        private static int pad = 0;

        public static int Max
        {
            get { return max; }
            set { max = value; }
        }

        public static int Min
        {
            get { return min; }
            set { min = value; }
        }

        public static int Padding
        {
            get { return pad; }
            set { pad = value; }
        }
        #endregion

        #region Ctors/Dtors
        public NaturalNumberGenome()
            :base()
        {

        }

        public NaturalNumberGenome(int size)
            :base(size)
        {

        }

        public NaturalNumberGenome(int size, bool permutation)
            :base(size, permutation)
        {

        }
        #endregion

        protected override void RandomEncoding()
        {
            for (int i = 0; i < size; i++)
            {
                this[i] = random.Next(min, max) + pad;
            }
        }

        protected override void PermutationEncoding()
        {
            bool hit = false;
            for (int i = 0; i < size; i++)
            {
                int chromo = random.Next(min, max) + pad;

                if (i == 0)
                {
                    this[i] = chromo;
                }
                else
                {
                    do
                    {
                        chromo = random.Next(min, max) + pad;

                        for (int x = 0; x < i; x++)
                        {
                            if (this[x] == chromo)
                            {
                                hit = true;
                                break;
                            }
                        }

                        if (!hit)
                        {
                            this[i] = chromo;
                        }

                    } while (hit);
                }

                hit = false;
            }
        }

        public override string ToString()
        {
            string str = "NaturalNumberGenome";
            str += base.ToString();

            return str;
        }

    }
}
