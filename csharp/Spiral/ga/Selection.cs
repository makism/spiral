using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace spiral.ga
{
    public enum SelectionType
    {
        RouletteWheel,
        Tournament
    }

    public class Selection<T>
    {

        public static T RouletteWheel(Pool<T> pool)
        {
            return default(T);
        }

    }
}
